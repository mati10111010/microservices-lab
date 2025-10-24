from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView # La crearemos en el Paso 3

urlpatterns = [
    # Rutas para JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Obtiene el access y refresh token 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresca el access token 
    # Ruta personalizada para el registro (la implementaremos)
    path('register/', RegisterView.as_view(), name='register'), # Crea un nuevo usuario
]