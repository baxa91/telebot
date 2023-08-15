from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core import settings

schema_view = get_schema_view(
    openapi.Info(
        title='TEST API',
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('api/', include('auth_user.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
