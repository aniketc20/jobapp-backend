from django.urls import include, path
from rest_framework import routers
from users.views import *
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('user/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
