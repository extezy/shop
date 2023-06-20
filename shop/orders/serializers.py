from rest_framework import serializers
from orders.models import Order, OrderItem
from online_shop.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ('product', 'price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Order
        fields = (
            'user',
            'first_name',
            'last_name',
            'phone',
            'address',
            'postal_code',
            'items',
            'total_cost',
            'created'
        )

        extra_kwargs = {
            'user': {'required': False},
        }

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
