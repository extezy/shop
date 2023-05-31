from rest_framework.test import APITestCase
from django.urls import reverse
from clients.models import Client
from django.contrib.auth.models import User
from rest_framework import status

from clients.serializers import ClientSerializer


class ClientsApiTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='manson', email='manson@google.com', first_name='Vasya',
                                          last_name='Entrop')
        self.client_1 = Client.objects.create(user=self.user_1, gender='M', age=27, phone='+75642185479', full_address='Moscow')

        self.user_2 = User.objects.create_user(username='sara', email='sara@google.com', first_name='Sara',
                                          last_name='Maddison')
        self.client_2 = Client.objects.create(user=self.user_2, gender='F', age=30, phone='+72657841598', full_address='Paris')
        self.url = reverse('client-list')

    def test_get(self):
        response = self.client.get(self.url)

        serializer_data = ClientSerializer([self.client_1, self.client_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_clients_view_performance(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.url)

        self.assertEqual(len(response.data), 2)

        user_3 = User.objects.create_user(username='nikon', email='nikon@google.com', first_name='Nik',
                                          last_name='Maddison')
        Client.objects.create(user=user_3, gender='M', age=31, phone='+72654851598', full_address='Boston')

        with self.assertNumQueries(1):
            response = self.client.get(self.url)

        self.assertEqual(len(response.data), 3)
