from django.core.cache import cache
from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.conf import settings

@shared_task(base=Singleton)
def set_price(session_id):
    """ Task for count total price in Cart """
    from cart.models import Cart

    with transaction.atomic():
        cart = Cart.objects.select_for_update().get(session_id=session_id)
        cart_products = cart.cart_products.all()
        total_cost = sum([cart_product.quantity * cart_product.product.price for cart_product in cart_products])
        cart.total_cost = total_cost
        cart.save()

    cache.delete(settings.CART_SESSION_ID)
