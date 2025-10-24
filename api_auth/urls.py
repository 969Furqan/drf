from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('tokens/', obtain_auth_token, name = 'api_auth_token'),
    path('JWTToken/referesh/', TokenRefreshView.as_view(), name = 'jwt_referesh_token'),
    path('JWTToken/', TokenObtainPairView.as_view(), name='jwt_token'),
    ]