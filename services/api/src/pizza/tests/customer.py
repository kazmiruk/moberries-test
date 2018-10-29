from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pizza.models.customer import Customer


class CustomerTestCase(APITestCase):
    def test_create_customer(self):
        url = reverse('api-v1:customers-list')
        data = {'first_name': 'Bob', 'last_name': 'Smith'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        customer = Customer.objects.get()
        self.assertEqual(customer.first_name, data['first_name'])
        self.assertEqual(customer.last_name, data['last_name'])

    def test_delete_customer(self):
        customer = Customer.objects.create(first_name='Bob', last_name='Smith')
        self.assertFalse(customer.is_deleted)

        url = reverse('api-v1:customers-detail', kwargs={'pk': customer.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertTrue(Customer.objects.get().is_deleted)

    def test_update_customer(self):
        customer = Customer.objects.create(first_name='Bob', last_name='Smith')

        url = reverse('api-v1:customers-detail', kwargs={'pk': customer.id})
        data = {'first_name': 'Jack', 'last_name': 'Brown'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer = Customer.objects.get()
        self.assertEqual(customer.first_name, data['first_name'])
        self.assertEqual(customer.last_name, data['last_name'])

    def test_list_customers(self):
        first_customer = Customer.objects.create(first_name='Bob', last_name='Smith')
        second_customer = Customer.objects.create(first_name='Jack', last_name='Brown')

        url = reverse('api-v1:customers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], first_customer.id)
        self.assertEqual(response.data[1]['id'], second_customer.id)

    def test_get_customer(self):
        customer = Customer.objects.create(first_name='Bob', last_name='Smith')

        url = reverse('api-v1:customers-detail', kwargs={'pk': customer.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], customer.id)
        self.assertEqual(response.data['first_name'], customer.first_name)
        self.assertEqual(response.data['last_name'], customer.last_name)

    def test_get_no_customer(self):
        url = reverse('api-v1:customers-detail', kwargs={'pk': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_no_customer(self):
        url = reverse('api-v1:customers-detail', kwargs={'pk': 404})
        data = {'first_name': 'Jack', 'last_name': 'Brown'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_customer(self):
        customer_data = {'first_name': 'Bob', 'last_name': 'Smith'}
        customer = Customer.objects.create(**customer_data)

        url = reverse('api-v1:customers-detail', kwargs={'pk': customer.id})
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        customer = Customer.objects.get()
        self.assertEqual(customer.first_name, customer_data['first_name'])
        self.assertEqual(customer.last_name, customer_data['last_name'])

    def test_create_invalid_customer(self):
        url = reverse('api-v1:customers-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 0)
