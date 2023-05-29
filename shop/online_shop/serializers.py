from rest_framework import serializers

from online_shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'image',
                  'description', 'price', 'stock', 'available')
