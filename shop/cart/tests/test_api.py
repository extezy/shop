import json

from rest_framework.test import APITestCase
from online_shop.models import Category, Product
from cart.models import Cart, ProductCart
from django.urls import reverse
from rest_framework import status


class CartApiTestCase(APITestCase):
    def setUp(self) -> None:
        url = reverse('cart-list')
        response = self.client.get(url)
        self.session_id = response.client.session.get('cart')

        self.cart_1 = Cart.objects.get(session_id=self.session_id)
        self.category_1 = Category.objects.create(name='Bathroom', slug='bathroom')
        self.category_2 = Category.objects.create(name='Kitchen', slug='kitchen')

        self.product_1 = Product.objects.create(
            name='Toothpaste',
            slug='toothpaste',
            category=self.category_1,
            description='Paste for tooth',
            price=5,
            stock=5,
            available=True
        )

        self.product_2 = Product.objects.create(
            name='Towel',
            slug='towel',
            category=self.category_2,
            description='Hand towel',
            price=2,
            stock=15,
            available=True)

        self.product_cart_1 = ProductCart.objects.create(cart=self.cart_1, product=self.product_1)
        self.product_cart_2 = ProductCart.objects.create(cart=self.cart_1, product=self.product_2)

    def test_get(self):
        self.maxDiff = None
        url = reverse('cart-list')

        expected_data = [{
            "session_id": self.session_id,
            "cart_products": [
                {
                    "product": {
                        "id": self.product_1.id,
                        "name": "Toothpaste",
                        "price": "5.00"
                    },
                    "quantity": 1,
                    "sub_cost": "5.00"
                },
                {
                    "product": {
                        "id": self.product_2.id,
                        "name": "Towel",
                        "price": "2.00"
                    },
                    "quantity": 1,
                    "sub_cost": "2.00"
                }
            ],
            "total_cost": "0.00"
        }]

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json.dumps(expected_data), json.dumps(response.data))

    def test_performance(self):
        product_3 = Product.objects.create(name='New', slug='new', category=self.category_2,
                                           description='new prod',
                                           price=5, stock=10, available=True)
        ProductCart.objects.create(cart=self.cart_1, product=product_3)

        url = reverse('cart-list')

        with self.assertNumQueries(8):
            response = self.client.get(url)

        self.assertEqual(3, len(response.data[0].get('cart_products')))

    def test_add_cart_product(self):
        url_post = reverse('product-add-list')
        post_data = {
            "product_id": self.product_1.id,
            "quantity": 2
        }

        response = self.client.post(path=url_post, data=post_data)

        expected_data = {
            "product_id": "Toothpaste",
            "quantity": 3
        }

        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)
        self.assertEqual(json.dumps(expected_data), json.dumps(response.data))

    def test_remove_cart_product(self):
        url_post = reverse('product-add-list')
        post_data = {
            "product_id": self.product_1.id,
            "quantity": 2
        }

        self.client.post(path=url_post, data=post_data)

        url_post = reverse('product-remove-list')

        post_data = {
            "product_id": self.product_1.id,
            "quantity": 1
        }

        remove_response = self.client.post(path=url_post, data=post_data)

        expected_data = {
            "product_id": "Toothpaste",
            "quantity": 2
        }

        self.assertEqual(status.HTTP_202_ACCEPTED, remove_response.status_code)
        self.assertEqual(json.dumps(expected_data), json.dumps(remove_response.data))

        post_data["quantity"] = 2
        remove_response = self.client.post(path=url_post, data=post_data)

        self.assertEqual(status.HTTP_204_NO_CONTENT, remove_response.status_code)
        self.assertEqual(json.dumps(None), json.dumps(remove_response.data))
