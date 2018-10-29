from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizza.models.order import Order
from pizza.serializers.customer_address import CustomerAddressSerializer
from pizza.serializers.pizza import PizzaSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('is_deleted', 'customer', )
        read_only_fields = ('id', 'ctime', 'mtime', )

    def validate(self, data):
        customer_address = data['customer_address']
        customer_id = int(self.context['view'].kwargs['customer_id'])

        if customer_address.customer_id != customer_id:
            raise ValidationError(detail='No such address for the customer')

        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)

        del response['customer_address']
        del response['size']

        response['address'] = CustomerAddressSerializer(instance.customer_address).data

        response['pizza'] = PizzaSerializer(instance.pizza).data
        response['pizza']['size'] = instance.size
        return response

    def create(self, validated_data):
        customer_id = self.context['view'].kwargs['customer_id']
        return Order.objects.create(customer_id=customer_id, **validated_data)

    def update(self, instance, validated_data):
        instance.customer_address = validated_data.get('customer_address', instance.customer_address)
        instance.pizza = validated_data.get('pizza', instance.pizza)
        instance.size = validated_data.get('size', instance.size)
        instance.save()
        return instance
