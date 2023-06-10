from rest_framework import serializers
from client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Client serializer"""
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'gender', 'age', 'phone', 'full_address')
