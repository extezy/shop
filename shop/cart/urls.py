from rest_framework import routers


from cart.views import CartView, CartResetView, ProductCartAddView, ProductCartRemoveView


client_router = routers.DefaultRouter()
client_router.register(r'api/cart', CartView)
client_router.register(r'api/reset_cart', CartResetView, basename='reset')
client_router.register(r'api/add_cart_product', ProductCartAddView, basename='product-add')
client_router.register(r'api/remove_cart_product', ProductCartRemoveView, basename='product-remove')


urlpatterns = [
]

urlpatterns += client_router.urls
