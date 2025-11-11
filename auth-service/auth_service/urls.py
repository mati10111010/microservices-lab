"""
URL configuration for auth_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication.views import RegisterUserView
urlpatterns = [
    path('admin/', admin.site.urls), # Ruta del administrador de Django
    # 1. Rutas para la generación de Tokens JWT (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # TokenObtainPairView: Genera el access token y refresh token (el login real)
    # 2. Ruta para refrescar el Token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # TokenRefreshView: Renueva el access token usando el refresh token
    # 3. Incluir las URLs de tu aplicación 'authentication'
    path('api/auth/', include('authentication.urls')),    # Usamos 'api/auth/' como prefijo para todas las rutas de la app
    path('register/', RegisterUserView.as_view(), name='register'),
]