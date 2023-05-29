from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from online_shop.models import Product
from online_shop.serializers import ProductSerializer


class ProductView(ReadOnlyModelViewSet):
    queryset = Product.objects.all().select_related('category').only('id',
                                                                     'name',
                                                                     'category__name',
                                                                     'image',
                                                                     'description',
                                                                     'price',
                                                                     'stock',
                                                                     'available')
    serializer_class = ProductSerializer
