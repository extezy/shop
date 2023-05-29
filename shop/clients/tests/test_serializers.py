from django.test import TestCase
from django.contrib.auth.models import User
from clients.models import Client
from clients.serializers import ClientSerializer


class ClientSerializerTestCase(TestCase):
    def test_ok(self):
        user_1 = User.objects.create_user(username='manson', email='manson@google.com', first_name='Vasya',
                                          last_name='Entrop')
        client_1 = Client.objects.create(user=user_1, gender='M', age=27, phone='+75642185479', full_address='Moscow')

        user_2 = User.objects.create_user(username='sara', email='sara@google.com', first_name='Sara',
                                          last_name='Maddison')
        client_2 = Client.objects.create(user=user_2, gender='F', age=30, phone='+72657841598', full_address='Paris')

        data = ClientSerializer([client_1, client_2], many=True).data
        expected_data = [
            {
                'id': client_1.id,
                'first_name': 'Vasya',
                'last_name': 'Entrop',
                'gender': 'M',
                'age': 27,
                'phone': '+75642185479',
                'full_address': 'Moscow'
            },
            {
                'id': client_2.id,
                'first_name': 'Sara',
                'last_name': 'Maddison',
                'gender': 'F',
                'age': 30,
                'phone': '+72657841598',
                'full_address': 'Paris'
            }
        ]

        self.assertEqual(expected_data, data)
