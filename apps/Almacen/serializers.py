from rest_framework import serializers
 
from apps.Almacen.models import Almacen
 

class AlmacenSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Almacen
        fields = '__all__'