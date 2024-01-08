from rest_framework import serializers
 
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.Venta.serilizers import VentaSerializerPostRegistro
from apps.Suscripcion.serializers import SuscripcionSerializerPostRegistro

class DetalleSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSuscripcion
        fields = '__all__'

class DetalleSuscripcionSerializerPostRegistro(serializers.ModelSerializer):
    idVenta = VentaSerializerPostRegistro()
    idSuscripcion = SuscripcionSerializerPostRegistro()
    class Meta:
        model = DetalleSuscripcion
        fields = ['idVenta','fechaInicio','fechaFin','idSuscripcion']