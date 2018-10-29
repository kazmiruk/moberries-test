import copy

from rest_framework import response, status

from pizza.models.customer import Customer


class CustomerNestedResourceMixin(object):
    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = copy.deepcopy(kwargs['data'])
            kwargs['data'].setdefault('customer_id', self.kwargs['customer_id'])

        return super().get_serializer(*args, **kwargs)

    def list(self, request, customer_id: int):
        customer = Customer.objects.filter(pk=customer_id).first()

        if customer is None:
            return response.Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        return super().list(request)

    def create(self, request, customer_id: int):
        customer = Customer.objects.filter(pk=customer_id).first()

        if customer is None:
            return response.Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        return super().create(request)
