from rest_framework import viewsets

from pizza.mixins.mark_as_deleted import MarkAsDeletedMixin
from pizza.models.customer import Customer
from pizza.serializers.customer import CustomerSerializer


class CustomerViewSet(MarkAsDeletedMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.filter(is_deleted=False)
    serializer_class = CustomerSerializer
