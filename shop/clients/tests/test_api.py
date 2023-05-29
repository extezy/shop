from rest_framework.test import APITestCase
from django.urls import reverse
from clients.models import Client
from django.contrib.auth.models import User
from rest_framework import status

from clients.serializers import ClientSerializer


class ClientsApiTestCase(APITestCase):
    def test_get(self):
        user_1 = User.objects.create_user(username='manson', email='manson@google.com', first_name='Vasya',
                                          last_name='Entrop')
        client_1 = Client.objects.create(user=user_1, gender='M', age=27, phone='+75642185479', full_address='Moscow')

        user_2 = User.objects.create_user(username='sara', email='sara@google.com', first_name='Sara',
                                          last_name='Maddison')
        client_2 = Client.objects.create(user=user_2, gender='F', age=30, phone='+72657841598', full_address='Paris')

        url = reverse('client-list')
        response = self.client.get(url)
        serializer_data = ClientSerializer([client_1, client_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
