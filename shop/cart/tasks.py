from celery import shared_task
from django.db.models import F


@shared_task
def set_price(session_id):
    """ Task for count total price in Cart """
    from cart.models import Cart

    cart = Cart.objects.get(session_id=session_id)
    cart_products = cart.cart_products.all()
    total_cost = sum([cart_product.quantity * cart_product.product.price for cart_product in cart_products])
    cart.total_cost = total_cost
    cart.save()
