from django.test import TestCase
from online_shop.models import Category, Product
from online_shop.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def test_ok(self):
        category_1 = Category.objects.create(name='Bathroom', slug='bathroom')
        category_2 = Category.objects.create(name='Kitchen', slug='kitchen')

        product_1 = Product.objects.create(name='Toothpaste', slug='toothpaste', category=category_1,
                                           description='Paste for tooth',
                                           price=5, stock=5, available=True)

        product_2 = Product.objects.create(name='Towel', slug='towel', category=category_2,
                                           description='Hand towel',
                                           price=2, stock=15, available=True)

        data = ProductSerializer([product_1, product_2], many=True).data

        expected_data = [
            {
                'id': product_1.id,
                'name': 'Toothpaste',
                'category': 'Bathroom',
                'image': None,
                'description': 'Paste for tooth',
                'price': '5.00',
                'stock': 5,
                'available': True
            },
            {
                'id': product_2.id,
                'name': 'Towel',
                'category': 'Kitchen',
                'image': None,
                'description': 'Hand towel',
                'price': '2.00',
                'stock': 15,
                'available': True
            }
        ]

        self.assertEqual(expected_data, data)
