from rest_framework import viewsets

from pizza.mixins.customer_nested_resource import CustomerNestedResourceMixin
from pizza.mixins.mark_as_deleted import MarkAsDeletedMixin
from pizza.models.customer_address import CustomerAddress
from pizza.serializers.customer_address import CustomerAddressSerializer


class CustomerAddressViewSet(CustomerNestedResourceMixin, MarkAsDeletedMixin, viewsets.ModelViewSet):
    serializer_class = CustomerAddressSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return CustomerAddress.objects.filter(customer_id=customer_id, is_deleted=False)
