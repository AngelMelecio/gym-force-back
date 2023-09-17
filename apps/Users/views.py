from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.Users.serializer import (
    CustomTokenObtainPairSerializer, CustomUserSerializer
)
from apps.Users.models import User

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        usuario = request.data.get('usuario', '')
        password = request.data.get('password', '')
        
        user = authenticate(
            usuario=usuario,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data) 
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'access': login_serializer.validated_data.get('access'),
                    'refresh': login_serializer.validated_data.get('refresh'),
                    'usuario': user_serializer.data,
                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
    
class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        Rtoken = request.data["refresh"]
        token = RefreshToken(Rtoken)
        token.blacklist()
        return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        