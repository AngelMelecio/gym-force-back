from rest_framework import serializers
 
from apps.Frase.models import Frase
 

class FraseSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Frase
        fields = '__all__'

class FraseSerializerToGet(serializers.ModelSerializer):
    class Meta:
        model = Frase
        fields = ['frase']