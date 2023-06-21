from django.db.models.signals import post_init
from django.dispatch import receiver

from orders.models import OrderItem


@receiver(post_init, sender=OrderItem)
def calculate_cost(sender, instance):
    instance.price = instance.product.price * instance.quantity
    instance.save()
