from rest_framework import serializers

from pizza.models.customer_address import CustomerAddress


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        exclude = ('is_deleted', 'customer', )
        read_only_fields = ('id', 'ctime', 'mtime', )

    def create(self, validated_data):
        customer_id = self.context['view'].kwargs['customer_id']
        return CustomerAddress.objects.create(customer_id=customer_id, **validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
