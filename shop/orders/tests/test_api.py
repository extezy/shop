from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from online_shop.models import Category, Product
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer


class OrdersApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='manson',
            password='12345',
            email='manson@google.com',
            first_name='Vasya',
            last_name='Entrop'
        )

        self.category_1 = Category.objects.create(name='Bathroom', slug='bathroom')
        self.category_2 = Category.objects.create(name='Kitchen', slug='kitchen')

        self.product_1 = Product.objects.create(name='Toothpaste', slug='toothpaste', category=self.category_1,
                                                description='Paste for tooth',
                                                price=5, stock=5, available=True)

        self.product_2 = Product.objects.create(name='Towel', slug='towel', category=self.category_2,
                                                description='Hand towel',
                                                price=2, stock=15, available=True)

        self.order = Order.objects.create(
            user=self.user,
            first_name="Nick",
            last_name="Horsen",
            phone='+79587467547',
            address="Paris",
            postal_code="090807",
            total_cost=50,
        )

        self.order_item_1 = OrderItem.objects.create(
            order=self.order,
            product=self.product_1,
            price=25,
            quantity=5
        )

        self.order_item_2 = OrderItem.objects.create(
            order=self.order,
            product=self.product_2,
            price=30,
            quantity=4
        )

    def test_get(self):
        self.client.login(username='manson', password='12345')

        url = reverse('order-list')
        response = self.client.get(url)
        serializer_data = [OrderSerializer(self.order).data]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
