from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from online_shop.models import Product, Category
from online_shop.permissions import IsStaffOrAdminOrReadOnly
from online_shop.serializers import ProductSerializer, CategorySerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()

    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_sub', ]
    search_fields = ['name', 'sub_category']
    ordering_fields = ['name', ]
    permission_classes = [IsStaffOrAdminOrReadOnly, ]


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
    permission_classes = [IsStaffOrAdminOrReadOnly, ]


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """Root api point"""
    return Response({
        'product': reverse('product-list', request=request, format=format),
        'clients': reverse('client-list', request=request, format=format),
        'cart': reverse('cart-list', request=request, format=format),
        'reset_cart': reverse('reset-list', request=request, format=format),
        'add_cart_product': reverse('product-add-list', request=request, format=format),
        'remove_cart_product': reverse('product-remove-list', request=request, format=format),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def healthcheck(requset, format=None):
    """ Healthcheck """
    return Response(status=status.HTTP_200_OK)
