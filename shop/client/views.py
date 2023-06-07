from rest_framework.viewsets import ModelViewSet
from client.models import Client
from client.permissions import IsOwnerOrStaffOrAdmin
from client.serializers import ClientSerializer
from rest_framework.decorators import api_view
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
    permission_classes = (IsOwnerOrStaffOrAdmin,)


@api_view(["POST",])
def logout(request):
    if request.method == "POST":
        print(request.user)
        request.user.auth_token.delete()

    return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)
