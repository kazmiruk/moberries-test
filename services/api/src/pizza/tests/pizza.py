from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pizza.models.pizza import Pizza


class PizzaTestCase(APITestCase):
    def test_create_pizza(self):
        url = reverse('api-v1:pizzas-list')
        data = {'name': 'New test pizza'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pizza.objects.count(), 1)
        self.assertEqual(Pizza.objects.get().name, data['name'])

    def test_delete_pizza(self):
        pizza = Pizza.objects.create(name='New test pizza')
        self.assertFalse(pizza.is_deleted)

        url = reverse('api-v1:pizzas-detail', kwargs={'pk': pizza.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pizza.objects.count(), 1)
        self.assertTrue(Pizza.objects.get().is_deleted)

    def test_update_pizza(self):
        pizza = Pizza.objects.create(name='New test pizza')

        url = reverse('api-v1:pizzas-detail', kwargs={'pk': pizza.id})
        data = {'name': 'New test pizza (updated)'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Pizza.objects.get().name, data['name'])

    def test_list_pizzas(self):
        first_pizza = Pizza.objects.create(name='New test pizza 1')
        second_pizza = Pizza.objects.create(name='New test pizza 2')

        url = reverse('api-v1:pizzas-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], first_pizza.id)
        self.assertEqual(response.data[1]['id'], second_pizza.id)

    def test_get_pizza(self):
        pizza_name = 'New test pizza'
        pizza = Pizza.objects.create(name=pizza_name)

        url = reverse('api-v1:pizzas-detail', kwargs={'pk': pizza.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], pizza.id)
        self.assertEqual(response.data['name'], pizza_name)

    def test_get_no_pizza(self):
        url = reverse('api-v1:pizzas-detail', kwargs={'pk': 404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_no_pizza(self):
        url = reverse('api-v1:pizzas-detail', kwargs={'pk': 404})
        data = {'name': 'New test pizza (updated)'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_pizza(self):
        pizza_name = 'New test pizza'
        pizza = Pizza.objects.create(name=pizza_name)

        url = reverse('api-v1:pizzas-detail', kwargs={'pk': pizza.id})
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Pizza.objects.get().name, pizza_name)

    def test_create_invalid_pizza(self):
        url = reverse('api-v1:pizzas-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Pizza.objects.count(), 0)
