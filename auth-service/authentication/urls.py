from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Importamos las vistas de la aplicación
from .views import RegisterUserView, UserDetailView, UserListView 

urlpatterns = [
    # Rutas de Simple JWT (Login y Refresh)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # [POST] /api/auth/token/ - Para generar access y refresh token (Login)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # [POST] /api/auth/token/refresh/ - Para renovar el access token
    # Rutas de la App Authentication
    path('register/', RegisterUserView.as_view(), name='register'), # [POST] /api/auth/register/ - Para crear un nuevo usuario
    path('me/', UserDetailView.as_view(), name='user_detail'), # [GET/PUT/PATCH] /api/auth/me/ - Para obtener/actualizar el perfil del usuario autenticado
    path('list/', UserListView.as_view(), name='user_list'), # [GET] /api/auth/list/ - Listar todos los usuarios
]