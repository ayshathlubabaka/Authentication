from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),
]