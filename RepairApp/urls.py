from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from organization.views import get_csrf_token, MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/org/', include('organization.urls')),
    path('api/repair/', include('repair.urls')),
    path('api/eva/', include('evaluation.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('api/csrf-token/', get_csrf_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/wxlogin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
