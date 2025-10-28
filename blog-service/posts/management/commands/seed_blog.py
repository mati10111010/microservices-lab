import random
from uuid import uuid4 # Usamos UUID para simular IDs de autor externos
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from posts.models import Category, Post
# Datos de prueba
CATEGORIES = [
    "Microservicios", 
    "Python & Django", 
    "Docker", 
    "Arquitectura", 
    "Bases de Datos"
]
POST_TITLES = [
    "Optimización de Consultas N+1",
    "Introducción a la Arquitectura Hexagonal",
    "Caching con Redis en DRF",
    "Docker Compose para Microservicios",
    "Diseño de APIs RESTful Limpias",
    "Ventajas de usar PostgreSQL",
    "Patrones de Comunicación entre Servicios",
    "JWT y Autenticación en Django",
    "Testing en Servicios Distribuidos",
]
class Command(BaseCommand):
    help = 'Seeds the database with initial categories and posts for testing.'

    def handle(self, *args, **options):
        self.stdout.write("--- Iniciando Seeder de Blog ---")
        
        # Limpiar datos existentes
        Post.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING("Datos existentes borrados."))

        # Crear Categorías
        created_categories = {}
        for name in CATEGORIES:
            category, created = Category.objects.get_or_create(name=name, slug=slugify(name))
            created_categories[name] = category
            
        self.stdout.write(self.style.SUCCESS(f"{len(created_categories)} Categorías creadas."))
        
        # Crear Posts
        posts_to_create = []
        author_id_simulado = uuid4() # Usamos un solo ID de autor para simplificar

        for i, title in enumerate(POST_TITLES * 2): # Duplicamos para tener más posts
            # Selección aleatoria
            category_name = random.choice(CATEGORIES)
            category_obj = created_categories[category_name]
            
            # Contenido de ejemplo
            body_content = (
                f"Este es el contenido completo del artículo '{title}'. "
                "Aquí se discuten las mejores prácticas y técnicas para implementar "
                "un sistema escalable. Esto simula un texto largo para la vista de detalle. "
                "El microservicio de blog ya está configurado para caching con Redis y optimización N+1."
            )
            
            # Crear el objeto Post
            post = Post(
                title=f"{title} (ID {i+1})",
                slug=slugify(f"{title} id {i+1}"),
                excerpt=body_content[:150] + "...",
                body=body_content,
                category=category_obj,
                author_id=author_id_simulado,
                author_display_name="Dev Tester",
                views=random.randint(10, 500),
                status=random.choice(['published', 'draft', 'published', 'published'])
            )
            posts_to_create.append(post)
            
        Post.objects.bulk_create(posts_to_create)
        self.stdout.write(self.style.SUCCESS(f"{len(posts_to_create)} Posts creados y publicados."))
        self.stdout.write("--- Seeder de Blog Finalizado ---")