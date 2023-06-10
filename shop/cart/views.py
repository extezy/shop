from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, \
    ListModelMixin
from cart.models import Cart, ProductCart
from cart.serializers import CartSerializer, ProductCartAddDeleteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from online_shop.models import Product
from shop.settings import CART_SESSION_ID


class CartView(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            session_id = request.session.get(CART_SESSION_ID)
            cart, created = Cart.objects.get_or_create(session_id=session_id)
            request.session[CART_SESSION_ID] = str(cart.session_id)
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            session_id = request.session.get(CART_SESSION_ID)
            cart, created = Cart.objects.get_or_create(session_id=session_id)
            request.session[CART_SESSION_ID] = str(cart.session_id)
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CartResetView(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            session_id = request.session.get(CART_SESSION_ID)
            if session_id:
                cart = Cart.objects.get(session_id=session_id)
                cart.reset_products()
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(CartSerializer(cart).data, status=status.HTTP_205_RESET_CONTENT)


class ProductCartAddView(CreateModelMixin, GenericViewSet):
    queryset = ProductCart.objects.all()
    serializer_class = ProductCartAddDeleteSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            session_id = request.session.get(CART_SESSION_ID)
            cart, created = Cart.objects.get_or_create(session_id=session_id)
            request.session[CART_SESSION_ID] = str(cart.session_id)

            product_id = request.data.get('product_id')
            if not product_id:
                return Response({'product_id': 'is required', 'quantity': 'default 1'},
                                status=status.HTTP_400_BAD_REQUEST)
            quantity = request.data.get('quantity') or 1

            product_in_cart = ProductCart.objects.all().filter(product_id=product_id, cart=cart).first()
            if product_in_cart:
                product_in_cart.quantity += quantity
                product_in_cart.save()
            else:
                product_in_cart = ProductCart.objects.create(cart=cart, product=Product.objects.get(id=product_id))
                product_in_cart.save()
            return Response(ProductCartAddDeleteSerializer(product_in_cart).data, status=status.HTTP_202_ACCEPTED)


class ProductCartRemoveView(CreateModelMixin, GenericViewSet):
    queryset = ProductCart.objects.all()
    serializer_class = ProductCartAddDeleteSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            session_id = request.session.get(CART_SESSION_ID)
            cart, created = Cart.objects.get_or_create(session_id=session_id)
            request.session[CART_SESSION_ID] = str(cart.session_id)

            product_id = request.data.get('product_id')
            if not product_id:
                return Response({'product_id': 'is required', 'quantity': 'default 1'},
                                status=status.HTTP_400_BAD_REQUEST)
            quantity = request.data.get('quantity') or 1

            product_in_cart = ProductCart.objects.all().filter(product_id=product_id, cart=cart).first()

            if product_in_cart:
                if product_in_cart.quantity <= quantity:
                    product_in_cart.delete()
                    return Response(None, status=status.HTTP_204_NO_CONTENT)
                else:
                    product_in_cart.quantity -= quantity
                    product_in_cart.save()
            else:
                Response({"Have no this product in cart"}, status=status.HTTP_204_NO_CONTENT)
            return Response(ProductCartAddDeleteSerializer(product_in_cart).data, status=status.HTTP_202_ACCEPTED)
