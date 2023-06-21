from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .yasg import urlpatterns as doc_urls

from online_shop.views import auth


urlpatterns = [


    path('admin/', admin.site.urls),
    path('', include('online_shop.urls')),
    path('', include('client.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    url('', include('social_django.urls', namespace='social')),

    path('base-auth/', include('rest_framework.urls')),
    path('social-auth', auth, name='social-auth')
]

urlpatterns += doc_urls
