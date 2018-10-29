from rest_framework import viewsets

from pizza.mixins.customer_nested_resource import CustomerNestedResourceMixin
from pizza.mixins.mark_as_deleted import MarkAsDeletedMixin
from pizza.models.order import Order
from pizza.serializers.order import OrderSerializer


class OrderViewSet(CustomerNestedResourceMixin, MarkAsDeletedMixin, viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Order.objects.filter(customer_id=customer_id, is_deleted=False)
