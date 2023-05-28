from rest_framework import routers

from online_shop.views import ProductView


online_shop_router = routers.DefaultRouter()
online_shop_router.register(r'api/product', ProductView)
