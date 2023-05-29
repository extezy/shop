from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.models import User
from clients.models import Client
from clients.serializers import ClientSerializer


class ClientView(ReadOnlyModelViewSet):
    queryset = Client.objects.all().select_related('user').only('id',
                                                                'user__first_name',
                                                                'user__last_name',
                                                                'gender',
                                                                'age',
                                                                'phone',
                                                                'full_address'
    )

    serializer_class = ClientSerializer
