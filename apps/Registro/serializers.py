from rest_framework import serializers
 
from apps.Registro.models import Registro
 

class RegistroSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Registro
        fields = '__all__'

class RegistroSerializerToReport(serializers.ModelSerializer):
    nombre_cliente = serializers.CharField(source='idCliente.get_full_name')
    nombre_usuario = serializers.CharField(source='idUser.get_full_name')
    class Meta:
        model = Registro
        fields = ['nombre_cliente','nombre_usuario','fecha']