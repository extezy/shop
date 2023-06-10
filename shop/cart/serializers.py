from rest_framework import serializers
from cart.models import Cart, ProductCart
from online_shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class ProductCartAddDeleteSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product')

    class Meta:
        model = ProductCart
        fields = ('product_id', 'quantity')


class ProductCartSerializer(serializers.ModelSerializer):
    """ Product cart serializer """
    product = ProductSerializer(many=False)
    sub_cost = serializers.SerializerMethodField(method_name='cost')

    class Meta:
        model = ProductCart
        fields = ('product', 'quantity', 'sub_cost')

    def cost(self, product_cart: ProductCart):
        return str(product_cart.quantity * product_cart.product.price)


class CartSerializer(serializers.ModelSerializer):
    """ Cart serializer """
    session_id = serializers.UUIDField(read_only=True)
    cart_products = ProductCartSerializer(many=True)
    total_cost = serializers.SerializerMethodField(method_name='get_total_cost')

    class Meta:
        model = Cart
        fields = ('session_id', 'cart_products', 'total_cost')

    def get_total_cost(self, cart: Cart):
        cart_products = cart.cart_products.all()
        total_cost = sum([cart_product.quantity * cart_product.product.price for cart_product in cart_products])
        return str(total_cost)
