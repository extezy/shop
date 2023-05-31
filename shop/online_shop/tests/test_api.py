from rest_framework.test import APITestCase
from online_shop.models import Category, Product
from django.urls import reverse
from rest_framework import status

from online_shop.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.category_1 = Category.objects.create(name='Bathroom', slug='bathroom')

        self.product_1 = Product.objects.create(name='Toothpaste', slug='toothpaste', category=self.category_1,
                                   description='Paste for tooth',
                                   price=5, stock=3, available=True)

        self.category_2 = Category.objects.create(name='Kitchen', slug='kitchen')
        self.product_2 = Product.objects.create(name='Kitchen Towel', slug='towel', category=self.category_2,
                                           description='Hand towel',
                                           price=2, stock=15, available=True)

        self.product_3 = Product.objects.create(name='Knife', slug='knife', category=self.category_2,
                                                description='Kitchen knife',
                                                price=5, stock=1, available=True)

        self.url_list = reverse('product-list')

    def test_get(self):

        response = self.client.get(self.url_list)

        serializer_data = ProductSerializer([self.product_2, self.product_3,  self.product_1], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_list_product_view_performance(self):

        with self.assertNumQueries(1):
            response = self.client.get(self.url_list)

        self.assertEqual(len(response.data), 3)

        category = Category.objects.create(name='Test', slug='test')
        Product.objects.create(name='Towel', slug='towel', category=category,
                                           description='Hand towel',
                                           price=20, stock=10, available=True)

        with self.assertNumQueries(1):
            response = self.client.get(self.url_list)

        self.assertEqual(len(response.data), 4)

    def test_get_search(self):
        response = self.client.get(self.url_list, data={'search': 'Kitchen'})
        serializer_data = ProductSerializer([self.product_2, self.product_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        response = self.client.get(self.url_list, data={'ordering': '-stock'})
        serializer_data = ProductSerializer([self.product_2, self.product_1, self.product_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        response = self.client.get(self.url_list, data={'price': 5})
        serializer_data = ProductSerializer([self.product_3, self.product_1], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
