from django.test import TestCase
from online_shop.models import Product, Category


class CategoryModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        category = Category.objects.create(name='Bathroom', slug='bathroom')

        cls.category = category

    def test_str_return(self):
        category = CategoryModelTest.category
        self.assertEqual('Bathroom', category.__str__())

    def test_absolute_path(self):
        pass # TODO if it need to test


class ProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        category = Category.objects.create(name='Bathroom', slug='bathroom')
        product = Product.objects.create(name='Toothpaste', slug='toothpaste', category=category,
                                           description='Paste for tooth',
                                           price=5, stock=5, available=True)

        cls.product = product

    def test_str_product(self):
        product = ProductModelTest.product
        self.assertEqual('Toothpaste', product.__str__())

    def test_absolute_path(self):
        pass # TODO if it need to test