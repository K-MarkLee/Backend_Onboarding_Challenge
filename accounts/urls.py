from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = "accounts"

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('refresh', views.RefreshView.as_view(), name='refresh'),
]