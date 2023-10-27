from rest_framework import serializers
 
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.Venta.serilizers import VentaSerializerPostRegistro

class DetalleSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSuscripcion
        fields = '__all__'

class DetalleSuscripcionSerializerPostRegistro(serializers.ModelSerializer):
    idVenta = VentaSerializerPostRegistro()
    class Meta:
        model = DetalleSuscripcion
        fields = ['idVenta','estado','fechaInicio','fechaFin']