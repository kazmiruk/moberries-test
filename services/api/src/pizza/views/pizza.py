from rest_framework import viewsets

from pizza.mixins.mark_as_deleted import MarkAsDeletedMixin
from pizza.models.pizza import Pizza
from pizza.serializers.pizza import PizzaSerializer


class PizzaViewSet(MarkAsDeletedMixin, viewsets.ModelViewSet):
    queryset = Pizza.objects.filter(is_deleted=False)
    serializer_class = PizzaSerializer
