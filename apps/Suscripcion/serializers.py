from rest_framework import serializers
from apps.Suscripcion.models import Suscripcion

class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'