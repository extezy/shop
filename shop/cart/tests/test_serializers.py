import json

from django.test import TestCase
from cart.models import ProductCart, Cart
from cart.serializers import ProductCartSerializer, CartSerializer, ProductCartAddDeleteSerializer, ProductSerializer
from online_shop.models import Product, Category


class ProductCartSerializerTestCase(TestCase):

    def test_ok(self):
        cart_1 = Cart.objects.create()
        category_1 = Category.objects.create(name='Bathroom', slug='bathroom')
        category_2 = Category.objects.create(name='Kitchen', slug='kitchen')
        product_1 = Product.objects.create(
            name='Toothpaste',
            slug='toothpaste',
            category=category_1,
            description='Paste for tooth',
            price=5,
            stock=5,
            available=True
        )

        product_2 = Product.objects.create(
            name='Towel',
            slug='towel',
            category=category_2,
            description='Hand towel',
            price=2,
            stock=15,
            available=True
        )
        product_cart_1 = ProductCart.objects.create(cart=cart_1, product=product_1)
        product_cart_2 = ProductCart.objects.create(cart=cart_1, product=product_2)

        result = ProductCartSerializer([product_cart_1, product_cart_2], many=True)

        expected_data = [
            {
                "product": {
                    "id": product_1.id,
                    "name": "Toothpaste",
                    "price": "5.00",
                },
                "quantity": 1,
                "sub_cost": '5'
            },
            {
                "product": {
                    "id": product_2.id,
                    "name": "Towel",
                    "price": "2.00"
                },
                "quantity": 1,
                "sub_cost": '2'
            }
        ]

        self.assertEqual(json.dumps(expected_data), json.dumps(result.data))


class CartSerializerTestCase(TestCase):
    def test_ok(self):
        cart_1 = Cart.objects.create()
        category_1 = Category.objects.create(name='Bathroom', slug='bathrooms')
        category_2 = Category.objects.create(name='Kitchen', slug='kitchens')
        product_1 = Product.objects.create(
            name='Toothpaste',
            slug='toothpastes',
            category=category_1,
            description='Paste for tooth',
            price=5,
            stock=5,
            available=True
        )

        product_2 = Product.objects.create(
            name='Towel',
            slug='towels',
            category=category_2,
            description='Hand towel',
            price=2,
            stock=15,
            available=True
        )
        ProductCart.objects.create(cart=cart_1, product=product_1, quantity=2)
        ProductCart.objects.create(cart=cart_1, product=product_2, quantity=5)

        result = CartSerializer(cart_1)

        expected_data = {
            "session_id": str(cart_1.session_id),
            "cart_products": [
                {
                    "product": {
                        "id": product_1.id,
                        "name": "Toothpaste",
                        "price": "5.00",
                    },
                    "quantity": 2,
                    "sub_cost": '10.00'
                },
                {
                    "product": {
                        "id": product_2.id,
                        "name": "Towel",
                        "price": "2.00",
                    },
                    "quantity": 5,
                    "sub_cost": '10.00'
                },
            ],
            "total_cost": '0.00'
        }

        self.assertEqual(json.dumps(expected_data), json.dumps(result.data))


class ProductCartAddDeleteSerializerTestCase(TestCase):
    def test_ok(self):
        cart_1 = Cart.objects.create()
        product_1 = Product.objects.create(
            name='Toothpaste',
            slug='toothpastes',
            category=None,
            description='Paste for tooth',
            price=5,
            stock=5,
            available=True
        )

        product_2 = Product.objects.create(
            name='Towel',
            slug='towels',
            category=None,
            description='Hand towel',
            price=2,
            stock=15,
            available=True
        )

        product_cart_1 = ProductCart.objects.create(cart=cart_1, product=product_1, quantity=10)
        product_cart_2 = ProductCart.objects.create(cart=cart_1, product=product_2, quantity=15)

        result = ProductCartAddDeleteSerializer([product_cart_1, product_cart_2], many=True)

        expected_data = [
            {
                "product_id": "Toothpaste",
                "quantity": 10
            },
            {
                "product_id": "Towel",
                "quantity": 15
            }
        ]

        self.assertEqual(json.dumps(expected_data), json.dumps(result.data))


class ProductSerializerTestCase(TestCase):
    def test_ok(self):
        category_1 = Category.objects.create(name='Bathroom', slug='bathrooms')
        category_2 = Category.objects.create(name='Kitchen', slug='kitchens')
        product_1 = Product.objects.create(
            name='Toothpaste',
            slug='toothpastes',
            category=category_1,
            description='Paste for tooth',
            price=5,
            stock=5,
            available=True
        )

        product_2 = Product.objects.create(
            name='Towel',
            slug='towels',
            category=category_2,
            description='Hand towel',
            price=2,
            stock=15,
            available=True
        )

        result = ProductSerializer([product_1, product_2], many=True)

        print(json.dumps(result.data))
