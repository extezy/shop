import uuid

from django.db import models
from online_shop.models import Product


class Cart(models.Model):
    """ Cart model """
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    def __str__(self):
        return str(self.session_id)

    def reset_products(self):
        for product in self.cart_products.all():
            product.delete()


class ProductCart(models.Model):
    """ Product in cart """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name}, {self.quantity}'
