from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pizza.enums import PIZZA_SIZES
from pizza.models.customer import Customer
from pizza.models.customer_address import CustomerAddress
from pizza.models.order import Order
from pizza.models.pizza import Pizza


class OrderTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name='Bob', last_name='Smith')
        self.customer_address = CustomerAddress.objects.create(address='Baker Street 221 b',
                                                               customer=self.customer)
        self.pizza = Pizza.objects.create(name='Napoletana')

    def test_create_order(self):
        url = reverse('api-v1:customer_orders-list', kwargs={'customer_id': self.customer.id})
        data = {'customer_address': self.customer_address.id,
                'pizza': self.pizza.id, 'size': PIZZA_SIZES[0][0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.customer_id, self.customer.id)
        self.assertEqual(order.customer_address_id, data['customer_address'])
        self.assertEqual(order.pizza_id, data['pizza'])
        self.assertEqual(order.size, data['size'])

    def test_delete_order(self):
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])
        self.assertFalse(order.is_deleted)

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': order.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 1)
        self.assertTrue(Order.objects.get().is_deleted)

    def test_update_order(self):
        pizza = Pizza.objects.create(name='New pizza')
        customer_address = CustomerAddress.objects.create(address='Stark Tower, 22-5',
                                                          customer=self.customer)
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': order.id})
        data = {'customer_address': customer_address.id,
                'pizza': pizza.id, 'size': PIZZA_SIZES[1][0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = Order.objects.get()
        self.assertEqual(order.customer_address_id, data['customer_address'])
        self.assertEqual(order.pizza_id, data['pizza'])
        self.assertEqual(order.size, data['size'])

    def test_list_customer_orders(self):
        first_order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                           pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])
        second_order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                            pizza_id=self.pizza.id, size=PIZZA_SIZES[1][0])

        url = reverse('api-v1:customer_orders-list', kwargs={'customer_id': self.customer.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], second_order.id)
        self.assertEqual(response.data[1]['id'], first_order.id)

    def test_list_no_customer(self):
        url = reverse('api-v1:customer_orders-list', kwargs={'customer_id': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_not_my_customer_order(self):
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])
        new_customer = Customer.objects.create(first_name='Jack', last_name='Brown')

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': new_customer.id,
                                                               'pk': order.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_not_my_customer_order(self):
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])
        new_customer = Customer.objects.create(first_name='Jack', last_name='Brown')

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': new_customer.id,
                                                               'pk': order.id})
        data = {'customer_address': self.customer_address.id,
                'pizza': self.pizza.id, 'size': PIZZA_SIZES[1][0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_customer_order(self):
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': order.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)

    def test_get_no_customer(self):
        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': 404, 'pk': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_no_customer(self):
        url = reverse('api-v1:customer_orders-list', kwargs={'customer_id': 404})
        data = {'customer_address': self.customer_address.id,
                'pizza': self.pizza.id, 'size': PIZZA_SIZES[1][0]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_no_order(self):
        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_no_customer(self):
        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': 404, 'pk': 404})
        data = {'customer_address': self.customer_address.id,
                'pizza': self.pizza.id, 'size': PIZZA_SIZES[1][0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_no_customer_order(self):
        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': 404})
        data = {'customer_address': self.customer_address.id,
                'pizza': self.pizza.id, 'size': PIZZA_SIZES[1][0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_customer_order(self):
        order_data = {'customer_address_id': self.customer_address.id, 'customer_id': self.customer.id,
                      'pizza_id': self.pizza.id, 'size': PIZZA_SIZES[0][0]}
        order = Order.objects.create(**order_data)

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': order.id})
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_order(self):
        url = reverse('api-v1:customer_orders-list', kwargs={'customer_id': self.customer.id})
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_update_order_with_not_my_address(self):
        new_customer = Customer.objects.create(first_name='Jack', last_name='Brown')
        new_address = CustomerAddress.objects.create(address='Stark Tower, 22-5', customer=new_customer)
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': order.id})
        data = {'customer_address': new_address.id,
                'pizza': self.pizza.id, 'size': PIZZA_SIZES[1][0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_with_invalid_size(self):
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': order.id})
        data = {'customer_address': self.customer_address.id,
                'pizza': self.pizza.id, 'size': 1000}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_with_invalid_pizza(self):
        order = Order.objects.create(customer_id=self.customer.id, customer_address_id=self.customer_address.id,
                                     pizza_id=self.pizza.id, size=PIZZA_SIZES[0][0])

        url = reverse('api-v1:customer_orders-detail', kwargs={'customer_id': self.customer.id,
                                                               'pk': order.id})
        data = {'customer_address': self.customer_address.id,
                'pizza': 404, 'size': PIZZA_SIZES[0][0]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
