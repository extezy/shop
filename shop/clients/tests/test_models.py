from django.test import TestCase
from clients.models import Client
from django.contrib.auth.models import User


class ClientModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user_1 = User.objects.create_user(username='manson', email='manson@google.com', first_name='Vasya',
                                          last_name='Entrop')
        cls.client = Client.objects.create(user=user_1, gender='M', age=27, phone='+75642185479', full_address='Moscow')

    def test_str_return(self):
        client = ClientModelTest.client
        self.assertEqual('Vasya Entrop', client.__str__())

