from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from online_shop.models import Product
from online_shop.serializers import ProductSerializer


class ProductView(ReadOnlyModelViewSet):
    queryset = Product.objects.all().prefetch_related('category')
    serializer_class = ProductSerializer
