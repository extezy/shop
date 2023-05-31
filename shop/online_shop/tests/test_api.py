from rest_framework.test import APITestCase
from online_shop.models import Category, Product
from django.urls import reverse
from rest_framework import status

from online_shop.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def test_get(self):
        category_1 = Category.objects.create(name='Bathroom', slug='bathroom')

        product_1 = Product.objects.create(name='Toothpaste', slug='toothpaste', category=category_1,
                                   description='Paste for tooth',
                                   price=5, stock=5, available=True)

        category_2 = Category.objects.create(name='Kitchen', slug='kitchen')
        product_2 = Product.objects.create(name='Towel', slug='towel', category=category_2,
                                           description='Hand towel',
                                           price=2, stock=15, available=True)

        url = reverse('product-list')

        response = self.client.get(url)

        serializer_data = ProductSerializer([product_1, product_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_list_product_view_performance(self):
        category_1 = Category.objects.create(name='Bathroom', slug='bathroom')

        Product.objects.create(name='Toothpaste', slug='toothpaste', category=category_1,
                                   description='Paste for tooth',
                                   price=5, stock=5, available=True)

        url = reverse('product-list')

        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(len(response.data), 1)

        category_2 = Category.objects.create(name='Kitchen', slug='kitchen')
        Product.objects.create(name='Towel', slug='towel', category=category_2,
                                           description='Hand towel',
                                           price=2, stock=15, available=True)

        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(len(response.data), 2)
