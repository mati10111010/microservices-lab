from django.db import models

class Category(models.Model):
    """Modelo para las Categorías de los posts."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories" # Para que aparezca bien en el Admin

    def __str__(self):
        return self.name
    
    # Pendiente: implementar save() para auto-generar el slug

class Post(models.Model):
    """Modelo para las Publicaciones (Posts) del blog."""
    
    # Campos obligatorios para el MVP
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    
    # Relación: Un Post tiene una Categoría (Foreign Key)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    
    # Campo para la búsqueda (slug), paginación (publicado/orden) y caché (vistas)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    
    # Nota: El campo 'author' (autor) se relaciona con el Auth-Service,
    # pero como es un microservicio independiente, usaremos un campo
    # de solo lectura o un FK al modelo de usuario de Auth, si se integrara localmente.
    # Por ahora, para el MVP, lo mantenemos simple.
    author_id = models.IntegerField(null=True, blank=True) # Usamos solo el ID del autor

    class Meta:
        ordering = ['-published_at'] # Ordenar por más reciente primero

    def __str__(self):
        return self.title