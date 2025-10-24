from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Modelo de Usuario Personalizado
# Define la estructura de la tabla de usuarios en PostgreSQL
class UserManager(BaseUserManager):
    def create_user(self, email, password=None): 
        if not email:
            raise ValueError("Email obligatorio")
        user = self.model(email=self.normalize_email(email)) 
        user.set_password(password) 
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 
    # Permite el inicio de sesion se haga por correo electronico 
    # en lugar de nombre de usuario
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

