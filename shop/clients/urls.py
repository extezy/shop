from rest_framework import routers

from clients.views import ClientView


clients_router = routers.DefaultRouter()
clients_router.register(r'api/client', ClientView)
