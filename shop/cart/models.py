import uuid

from django.db import models
from online_shop.models import Product
from cart.tasks import set_price


class Cart(models.Model):
    """ Cart model """
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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

    def save(self, *args, **kwargs):
        set_price.delay(str(self.cart.session_id))
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        set_price.delay(str(self.cart.session_id))
        return super().delete(*args, **kwargs)
