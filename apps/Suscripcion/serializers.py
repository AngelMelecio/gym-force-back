from rest_framework import serializers
from apps.Suscripcion.models import Suscripcion

class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'

class SuscripcionSerializerPostRegistro(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = ['tipo','modalidad']