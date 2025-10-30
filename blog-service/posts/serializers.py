from rest_framework import serializers
from .models import Category, Post

# Serializer para la relación Category (simple)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # Solo necesitamos el ID, nombre y slug para las categorías
        fields = ('id', 'name', 'slug') 

# Serializer principal para los Posts
class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer usado para la lista de posts.
    Incluye solo información esencial y relaciones anidadas.
    """
    
    # Serializador anidado para la categoría
    category = CategorySerializer(read_only=True)
    
    # Campo para el autor (solo ID)
    author_id = serializers.IntegerField(read_only=True) 
    author_display_name = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 
            'title', 
            'slug', 
            'author_id',
            'author_display_name',
            'category', 
            'published_at', 
            'views'
        )
        read_only_fields = ('slug', 'published_at', 'views', 'author_display_name', 'author_id')
        
class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer usado para la vista de detalle de un solo post.
    Incluye el campo 'body' completo.
    """
    category = CategorySerializer(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    author_display_name = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 
            'title', 
            'slug', 
            'body',  # <-- Campo completo aquí
            'author_id',
            'author_display_name',
            'category', 
            'published_at', 
            'views',
        )
        read_only_fields = ('slug', 'published_at', 'views', 'author_display_name', 'author_id')