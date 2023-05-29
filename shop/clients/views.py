from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from clients.serializers import ClientSerializer


class ClientView(ReadOnlyModelViewSet):
    queryset = Client.objects.all().prefetch_related('user')
    serializer_class = ClientSerializer
