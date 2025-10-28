from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import F # Para evitar condiciones de carrera en el contador de vistas
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Category
from .serializers import CategorySerializer, PostListSerializer, PostDetailSerializer

class HealthCheckAPIView(APIView):
    """
    Endpoint verificar el estado de salud del servicio.
    """
    permission_classes = [] # Permitir acceso público

    def get(self, request, *args, **kwargs):
        # basta con devolver un estado OK.
        return Response({"status": "ok", "service": "blog_service"}, status=status.HTTP_200_OK)

# Tiempo de caché en segundos (ej. 5 minutos)
CACHE_TTL_5MIN = 60 * 5 
CACHE_TTL_1HOUR = 60 * 60
@method_decorator(cache_page(CACHE_TTL_1HOUR), name='dispatch')
class CategoryListAPIView(generics.ListAPIView):
    """
    Endpoint para listar categorías con caché de 1 hora.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ['name',]
    # No necesita paginación, ya que la lista de categorías es pequeña
    pagination_class = None
class PostListAPIView(generics.ListAPIView):
    """
    Endpoint para listar posts.
    Incluye paginación, búsqueda por título/cuerpo y filtrado por categoría/status.
    """
    serializer_class = PostListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    
    # 1. Filtros personalizados (para filtrar por category__slug y status)
    filterset_fields = {
        'category__slug': ['exact'],
        'status': ['exact'],
    }
    # 2. Búsqueda por texto (server-side search)
    search_fields = ['title', 'body']
    
    # 3. Ordenamiento
    ordering_fields = ['published_at', 'views']
    ordering = ['-published_at']

    def get_queryset(self):
        # Optimización CRÍTICA: Evita consultas N+1
        return Post.objects.filter(status='published').select_related('category')

class PostDetailAPIView(generics.RetrieveAPIView):
    """Endpoint para el detalle de un post. Incrementa el contador de vistas.
    - Usa caché de detalle por 5 minutos. """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug' # Permite buscar por slug en la URL

@method_decorator(cache_page(CACHE_TTL_5MIN))
def get(self, request, *args, **kwargs):
    # Primero, llama al método GET de la clase base, que usa caché si está disponible
    response = super().get(request, *args, **kwargs)
        
    # Lógica para incrementar el contador de vistas (solo si la respuesta es exitosa)
    if response.status_code == 200:
        post = self.get_object()
            
        # Usamos F() para actualizar el contador a nivel de base de datos de forma atómica
        Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
            
        # Nota: El objeto 'post' en la respuesta cacheada tendrá el valor 'views' viejo.
        # Esto es aceptable para la mayoría de los casos de uso.
            
    return response