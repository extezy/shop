from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

import client.views
from client.views import ClientView
from django.urls import path, include


client_router = routers.DefaultRouter()
client_router.register(r'api/client', ClientView)

urlpatterns = [
    path('api/token/login/', obtain_auth_token),
    path('api/token/logout/', client.views.logout),
    path('api/base-auth', include('rest_framework.urls')),
]

urlpatterns += client_router.urls
