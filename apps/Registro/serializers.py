from rest_framework import serializers
 
from apps.Registro.models import Registro
 

class RegistroSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Registro
        fields = '__all__'

class RegistroSerializerToReport(serializers.ModelSerializer):
    nombre_usuario = serializers.CharField(source='idUser.get_full_name')    
    nombre_cliente = serializers.SerializerMethodField()

    class Meta:
        model = Registro
        fields = ['nombre_cliente','nombre_usuario','fecha']
        
    def get_nombre_cliente(self, obj):
        # Verifica si hay un cliente asociado y devuelve su nombre. Si no, devuelve una cadena vacía o un mensaje.
        if obj.idCliente:
            return obj.idCliente.get_full_name()
        return "Cliente no registrado"  # O lo que prefieras