from django.test import TestCase
from orders.serializers import OrderSerializer, OrderItemSerializer
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
from online_shop.models import Product, Category
import json


class OrderItemSerializerCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='123')

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
            total_cost=50
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

    def test_ok(self):
        data = OrderItemSerializer(self.order.items, many=True).data

        expected_data = [
            {
                "product":
                    {
                        "id": self.product_1.id,
                        "name": "Toothpaste",
                        "category":
                            {
                                "name": "Bathroom",
                                "slug": "bathroom",
                                "sub_category": None,
                                "is_sub": False
                            },
                        "image": None,
                        "description": "Paste for tooth",
                        "price": "5.00",
                        "stock": 5,
                        "available": True
                    },
                "price": "25.00",
                "quantity": 5
            },
            {
                "product":
                    {
                        "id": self.product_2.id,
                        "name": "Towel",
                        "category":
                            {
                                "name": "Kitchen",
                                "slug": "kitchen",
                                "sub_category": None,
                                "is_sub": False
                            },
                        "image": None,
                        "description": "Hand towel",
                        "price": "2.00",
                        "stock": 15,
                        "available": True
                    },
                "price": "30.00",
                "quantity": 4
            }
        ]

        self.assertEqual(json.dumps(expected_data), json.dumps(data))


class OrderSerializerCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='123')

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

    def test_ok(self):
        self.maxDiff = None
        data = OrderSerializer(self.order, many=False).data

        expected_data = {
            "user": self.user.id,
            "first_name": "Nick",
            "last_name": "Horsen",
            "phone": "+79587467547",
            "address": "Paris",
            "postal_code": "090807",
            "items":
                [
                    {
                        "product":
                            {
                                "id": self.product_1.id,
                                "name": "Toothpaste",
                                "category":
                                    {
                                        "name": "Bathroom",
                                        "slug": "bathroom",
                                        "sub_category": None,
                                        "is_sub": False
                                    },
                                "image": None,
                                "description": "Paste for tooth",
                                "price": "5.00",
                                "stock": 5,
                                "available": True
                            },
                        "price": "25.00",
                        "quantity": 5
                    },
                    {
                        "product":
                            {
                                "id": self.product_2.id,
                                "name": "Towel",
                                "category":
                                    {
                                        "name": "Kitchen",
                                        "slug": "kitchen",
                                        "sub_category": None,
                                        "is_sub": False
                                    },
                                "image": None,
                                "description": "Hand towel",
                                "price": "2.00",
                                "stock": 15,
                                "available": True
                            },
                        "price": "30.00",
                        "quantity": 4
                    }
                ],
            "total_cost": "50.00",

            "created": self.order.created.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.assertEqual(json.dumps(expected_data), json.dumps(data))
