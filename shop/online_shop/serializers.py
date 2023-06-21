from rest_framework import serializers

from online_shop.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'sub_category', 'is_sub')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)

    class Meta:
        ref_name = 'ShopProductSerializer'
        model = Product
        fields = ('id', 'name', 'category', 'image',
                  'description', 'price', 'stock',
                  'available')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)
        product = Product.objects.create(**validated_data, category=category)
        return product
