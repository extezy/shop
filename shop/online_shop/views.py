from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from online_shop.models import Product, Category
from online_shop.permissions import IsStaffOrAdminOrReadOnly
from online_shop.serializers import ProductSerializer, CategorySerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()

    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_sub',]
    search_fields = ['name', 'sub_category']
    ordering_fields = ['name',]
    permission_classes = [IsStaffOrAdminOrReadOnly,]


class ProductView(ModelViewSet):
    queryset = Product.objects.all().select_related('category').only('id',
                                                                     'name',
                                                                     'category',
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
    permission_classes = [IsStaffOrAdminOrReadOnly,]


@api_view(['GET'])
def api_root(request, format=None):
    """Root api point"""
    return Response({
        'product': reverse('product-list', request=request, format=format),
        'clients': reverse('client-list', request=request, format=format),
    })
