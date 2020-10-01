from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.api.views import TokenLifetimeView, RefreshLifetimeView

urlpatterns = [
    path('token/optain', TokenLifetimeView.as_view(), name='obtain-token'),
    path('token/refresh', RefreshLifetimeView.as_view(), name='obtain-refresh'),
]