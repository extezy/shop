from rest_framework import serializers
from django.contrib.auth.models import User
from clients.models import Client


class UserSerializer(serializers.ModelSerializer):
    """Django User serializer"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ClientSerializer(serializers.ModelSerializer):
    """Client serializer"""
    client_name = UserSerializer(source='user')

    class Meta:
        model = Client
        fields = ('id', 'client_name', 'gender', 'age', 'phone', 'full_address')
