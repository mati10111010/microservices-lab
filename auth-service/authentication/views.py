from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterUserSerializer, UserSerializer
from .models import User

# 1. Vista de Registro de Usuarios
class RegisterUserView(generics.CreateAPIView):
    """Permite el registro de nuevos usuarios.Endpoint: POST /api/auth/register/"""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # Permite el acceso a usuarios no autenticados
    serializer_class = RegisterUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context={'request': request}).data,
            "message": "Registro exitoso."
        }, status=status.HTTP_201_CREATED)

# 2. Vista de Detalle de Usuario (Perfil Propio)
class UserDetailView(generics.RetrieveUpdateAPIView):
    """Permite ver y actualizar los detalles del usuario autenticado.Endpoint: GET/PUT/PATCH /api/auth/me/"""
    permission_classes = [permissions.IsAuthenticated] # Solo acceso a usuarios autenticados
    serializer_class = UserSerializer
    def get_object(self):
        """Retorna el usuario actualmente autenticado."""
        return self.request.user
    
# 3. Vista de Listado de Usuarios (Solo Admin)
class UserListView(generics.ListAPIView):
    """Lista todos los usuarios registrados (solo accesible para staff).Endpoint: GET /api/auth/list/"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Usamos una política para asegurar que solo los usuarios staff (is_staff=True) pueden acceder
    permission_classes = [permissions.IsAdminUser]