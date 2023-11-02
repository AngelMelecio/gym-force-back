from rest_framework import serializers
from apps.Cliente.models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ClienteSerializerPostRegistro(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre','apellidos','idCliente']

