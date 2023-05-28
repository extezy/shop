from rest_framework import serializers

from online_shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category_name')

    class Meta:
        model = Product
        fields = ('id', 'name', 'category_name', 'image',
                  'description', 'price', 'stock', 'available')
