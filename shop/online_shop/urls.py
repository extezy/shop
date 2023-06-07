from rest_framework import routers

import online_shop.views
from online_shop.views import ProductView, CategoryView
from django.urls import path

online_shop_router = routers.DefaultRouter()
online_shop_router.register(r'api/product', ProductView)
online_shop_router.register(r'api/category', CategoryView)

urlpatterns = [
    path('', online_shop.views.api_root),
]

urlpatterns += online_shop_router.urls
