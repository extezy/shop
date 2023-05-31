from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price', 'category__name', 'available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock']
