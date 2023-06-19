from rest_framework.viewsets import ModelViewSet
from client.models import Client
from client.permissions import IsStaffOrAdmin
from rest_framework.permissions import IsAuthenticated
from client.serializers import ClientSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


class ClientView(ModelViewSet):
    queryset = Client.objects.all().select_related('user').only('id',
                                                                'user__first_name',
                                                                'user__last_name',
                                                                'gender',
                                                                'age',
                                                                'phone',
                                                                'full_address'
                                                                )

    serializer_class = ClientSerializer
    permission_classes = (IsStaffOrAdmin,)


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def profile(request):
    client, created = Client.objects.all().select_related('user').only('id',
                                                                       'user__first_name',
                                                                       'user__last_name',
                                                                       'gender',
                                                                       'age',
                                                                       'phone',
                                                                       'full_address'
                                                                       ).get_or_create(user=request.user)

    if request.method == "GET":
        return Response(ClientSerializer(client).data, status=status.HTTP_200_OK)


@api_view(["POST", ])
def logout(request):
    if request.method == "POST":
        print(request.user)
        request.user.auth_token.delete()

    return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)
