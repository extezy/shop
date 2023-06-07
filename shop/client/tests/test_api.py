from rest_framework.test import APITestCase
from django.urls import reverse
from client.models import Client
from django.contrib.auth.models import User
from rest_framework import status
from django.test import Client as TestClient
from rest_framework.test import APIClient
from client.serializers import ClientSerializer


class ClientsApiTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_superuser(username='manson', password='12345', email='manson@google.com', first_name='Vasya',
                                          last_name='Entrop')
        self.client_1 = Client.objects.create(user=self.user_1, gender='M', age=27, phone='+75642185479', full_address='Moscow')

        self.user_2 = User.objects.create_user(username='sara', password='54321', email='sara@google.com', first_name='Sara',
                                          last_name='Maddison', is_staff=True)
        self.client_2 = Client.objects.create(user=self.user_2, gender='F', age=30, phone='+72657841598', full_address='Paris')
        self.url = reverse('client-list')

        self.drf_login_in_client = APIClient()
        response = self.drf_login_in_client.post('/api/token/login/', {'username': 'manson', 'password': '12345'})
        self.drf_login_in_client.credentials(HTTP_AUTHORIZATION='Token ' + response.data.get('token'))

    def test_token_authorization(self):
        api_client = APIClient()
        response = api_client.post('/api/token/login/', {'username': 'sara', 'password': '54321'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data.get('token'))
        self.assertEqual(response.data.get('token'), str(self.user_2.auth_token))

        api_client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        response = api_client.post('/api/token/logout/', {'Authorization': self.user_2.auth_token})
        self.assertEqual({'Message': 'You are logged out'}, response.data)

    def test_basic_authenticate(self):
        login_client = TestClient()
        authenticated = login_client.login(username='manson', password='12345')
        self.assertTrue(authenticated)

    def test_get_permission(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get(self):

        response = self.drf_login_in_client.get(self.url)
        serializer_data = ClientSerializer([self.client_1, self.client_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_clients_view_performance(self):

        with self.assertNumQueries(2):
            response = self.drf_login_in_client.get(self.url)

        self.assertEqual(len(response.data), 2)

        user_3 = User.objects.create_user(username='nikon', email='nikon@google.com', first_name='Nik',
                                          last_name='Maddison')
        Client.objects.create(user=user_3, gender='M', age=31, phone='+72654851598', full_address='Boston')

        with self.assertNumQueries(2):
            response = self.drf_login_in_client.get(self.url)

        self.assertEqual(len(response.data), 3)
