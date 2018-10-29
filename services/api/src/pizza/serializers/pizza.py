from rest_framework import serializers

from pizza.models.pizza import Pizza


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        exclude = ('is_deleted', )
        read_only_fields = ('id', 'ctime', 'mtime',)

    def create(self, validated_data):
        return Pizza.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
