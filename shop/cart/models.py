import uuid
from django.db import models
from online_shop.models import Product
from cart.tasks import set_price
from orders.models import Order, OrderItem


class Cart(models.Model):
    """ Cart model """
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.session_id)

    def reset_products(self):
        for product in self.cart_products.all():
            product.delete()
        self.total_cost = 0

    def count_products(self):
        return self.cart_products.all().count()

    def cart_products_to_order_items(self, order: Order):
        for product_cart in self.cart_products.all():
            OrderItem.objects.create(
                order=order,
                product=product_cart.product,
                quantity=product_cart.quantity
            )


class ProductCart(models.Model):
    """ Product in cart """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name}, {self.quantity}'

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        session_id = str(self.cart.session_id)
        set_price.delay(session_id)
        return result

    def delete(self, *args, **kwargs):
        """ Delete object and recalculate cart"""
        session_id = str(self.cart.session_id)
        result = super().delete(*args, **kwargs)
        set_price.delay(session_id)
        return result
