from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView # La crearemos en el Paso 3

urlpatterns = [
    # Rutas para JWT
    # # Obtiene el access y refresh token (login)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    # Refresca el access token (renovacion)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    # Ruta personalizada para el registro (la implementaremos)
    # # Crea un nuevo usuario (registro de usuarios)
    path('register/', RegisterView.as_view(), name='register'), 
]