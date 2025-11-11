from rest_framework import serializers
from .models import User # Importamos el modelo User

class RegisterUserSerializer(serializers.ModelSerializer):
    # Campo extra para confirmar la contraseña
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate(self, data):
        """Valida que las dos contraseñas coincidan."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas deben coincidir."})
        return data

    def create(self, validated_data):
        """Crea y devuelve un nuevo usuario."""
        validated_data.pop('password2') # Eliminamos password2 antes de crear el usuario
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """Serializador simple para el detalle de usuario (perfil)."""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['email', 'date_joined']