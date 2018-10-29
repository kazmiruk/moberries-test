from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pizza.models.customer import Customer
from pizza.models.customer_address import CustomerAddress


class CustomerAddressTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name='Bob', last_name='Smith')

    def test_create_customer_address(self):
        url = reverse('api-v1:customer_addresses-list', kwargs={'customer_id': self.customer.id})
        data = {'address': 'Baker Street 221 b'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomerAddress.objects.count(), 1)
        customer_address = CustomerAddress.objects.get()
        self.assertEqual(customer_address.customer_id, self.customer.id)
        self.assertEqual(customer_address.address, data['address'])

    def test_delete_customer_address(self):
        customer_address = CustomerAddress.objects.create(customer_id=self.customer.id,
                                                          address='Baker Street 221 b')
        self.assertFalse(customer_address.is_deleted)

        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': self.customer.id,
                                                                  'pk': customer_address.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomerAddress.objects.count(), 1)
        self.assertTrue(CustomerAddress.objects.get().is_deleted)

    def test_update_customer_address(self):
        customer_address = CustomerAddress.objects.create(customer_id=self.customer.id,
                                                          address='Baker Street 221 b')

        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': self.customer.id,
                                                                  'pk': customer_address.id})
        data = {'address': 'Stark Tower, 22-5'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer_address = CustomerAddress.objects.get()
        self.assertEqual(customer_address.address, data['address'])

    def test_list_customer_addresses(self):
        first_address = CustomerAddress.objects.create(customer_id=self.customer.id,
                                                       address='Baker Street 221 b')
        second_address = CustomerAddress.objects.create(customer_id=self.customer.id,
                                                        address='Stark Tower, 22-5')

        url = reverse('api-v1:customer_addresses-list', kwargs={'customer_id': self.customer.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], first_address.id)
        self.assertEqual(response.data[1]['id'], second_address.id)

    def test_list_no_customer(self):
        url = reverse('api-v1:customer_addresses-list', kwargs={'customer_id': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_not_my_customer_addresses(self):
        customer_address = CustomerAddress.objects.create(customer_id=self.customer.id,
                                                          address='Baker Street 221 b')
        new_customer = Customer.objects.create(first_name='Jack', last_name='Brown')

        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': new_customer.id,
                                                                  'pk': customer_address.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_not_my_customer_addresses(self):
        customer_address = CustomerAddress.objects.create(customer_id=self.customer.id,
                                                          address='Baker Street 221 b')
        new_customer = Customer.objects.create(first_name='Jack', last_name='Brown')

        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': new_customer.id,
                                                                  'pk': customer_address.id})
        data = {'address': 'Stark Tower, 22-5'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_customer_address(self):
        customer_address = CustomerAddress.objects.create(customer_id=self.customer.id,
                                                          address='Baker Street 221 b')

        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': self.customer.id,
                                                                  'pk': customer_address.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], customer_address.id)
        self.assertEqual(response.data['address'], customer_address.address)

    def test_get_no_customer(self):
        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': 404, 'pk': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_no_customer(self):
        url = reverse('api-v1:customer_addresses-list', kwargs={'customer_id': 404})
        data = {'address': 'Baker Street 221 b'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_no_customer_address(self):
        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': self.customer.id,
                                                                  'pk': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_no_customer(self):
        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': 404, 'pk': 404})
        data = {'address': 'Stark Tower, 22-5'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_no_customer_address(self):
        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': self.customer.id,
                                                                  'pk': 404})
        data = {'address': 'Stark Tower, 22-5'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_customer_address(self):
        customer_address_data = {'customer_id': self.customer.id, 'address': 'Stark Tower, 22-5'}
        customer_address = CustomerAddress.objects.create(**customer_address_data)

        url = reverse('api-v1:customer_addresses-detail', kwargs={'customer_id': self.customer.id,
                                                                  'pk': customer_address.id})
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        customer_address = CustomerAddress.objects.get()
        self.assertEqual(customer_address.address, customer_address_data['address'])

    def test_create_invalid_customer_address(self):
        url = reverse('api-v1:customer_addresses-list', kwargs={'customer_id': self.customer.id})
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomerAddress.objects.count(), 0)
