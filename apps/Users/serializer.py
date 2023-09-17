from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.Users.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','usuario','correo','nombre','apellidos', 'is_active', 'is_staff', 'rol')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','usuario','correo','nombre','apellidos', 'is_active', 'is_staff', 'rol' ,'password')
    
    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','usuario','correo','nombre','apellidos', 'is_active', 'is_staff', 'rol')
    
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'nombre': instance['nombre'],
            'apellidos': instance['apellidos'],
            'usuario': instance['usuario'],
            'correo': instance['correo'],
            'is_staff': instance['is_staff'],
            'is_active': instance['is_active'],
            'rol': instance['rol']
        }