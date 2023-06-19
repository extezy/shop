from rest_framework import routers
from django.urls import path

import orders.views
from orders.views import OrderView

client_router = routers.DefaultRouter()
client_router.register(r'api/order', OrderView)


urlpatterns = [
    path(r'api/make_order', orders.views.make_order, name='make_order')
]

urlpatterns += client_router.urls
