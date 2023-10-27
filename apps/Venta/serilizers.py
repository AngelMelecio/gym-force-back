from rest_framework import serializers
 
from apps.Venta.models import Venta
from apps.Cliente.serializers import ClienteSerializerPostRegistro

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class VentaSerializerPostRegistro(serializers.ModelSerializer):
    idCliente = ClienteSerializerPostRegistro()
    class Meta:
        model = Venta
        fields = ['idCliente']