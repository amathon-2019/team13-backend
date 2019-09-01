from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import SocketAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/', 
        include(
            ('api.urls', 'api'),
            namespace='api'
        )
    ),
    path(
        'user/check/',
        SocketAPIView.as_view()
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
