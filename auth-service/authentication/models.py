from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Manager personalizado para crear usuarios
class CustomUserManager(BaseUserManager):
    """Manager de modelo personalizado donde el email es el identificador único para el inicio de sesión en lugar del username."""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('El email debe ser configurado.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """Crea y guarda un superusuario con el email y la contraseña dados."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('El superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('El superusuario debe tener is_superuser=True.'))
            
        return self.create_user(email, password, **extra_fields)

# Modelo de Usuario
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    # Campos de perfil
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    # Campos de estado y permisos
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False) # Añadido por seguridad
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Define el campo 'email' como el campo de inicio de sesión
    USERNAME_FIELD = 'email'
    # Campos adicionales requeridos al crear un usuario (aparte del USERNAME_FIELD y password)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email