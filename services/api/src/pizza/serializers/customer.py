from rest_framework import serializers

from pizza.models.customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('is_deleted', )
        read_only_fields = ('id', 'ctime', 'mtime', )

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
