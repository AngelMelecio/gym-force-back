from rest_framework import serializers
 
from apps.Registro.models import Registro
 

class RegistroSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Registro
        fields = '__all__'