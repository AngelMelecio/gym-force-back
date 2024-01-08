from rest_framework import serializers
from apps.Cliente.models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ClienteSerializerPostRegistro(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre','apellidos','idCliente','fotografia']


class ClienteRegistrosSerializer(serializers.ModelSerializer):
    hasHuella = serializers.SerializerMethodField('get_hasHuella')
    class Meta:
        model = Cliente
        fields = ['idCliente','nombre','apellidos','hasHuella']

    def get_hasHuella(self, obj):
        return obj.huella is not None