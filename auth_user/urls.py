from django.urls import include, path
from auth_user import views


urlpatterns = [
    path(r'auth/', include('djoser.urls')),
    path('send/', views.SendTelegramView.as_view(), name='send')
]
