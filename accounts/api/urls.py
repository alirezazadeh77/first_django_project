from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.api.views import TokenLifetimeView, RefreshLifetimeView, Register, SetPasswordView

urlpatterns = [
    path('token/obtain/', TokenLifetimeView.as_view(), name='obtain-token'),
    path('token/refresh/', RefreshLifetimeView.as_view(), name='obtain-refresh'),
    path('register/', Register.as_view(), name='register'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
]
