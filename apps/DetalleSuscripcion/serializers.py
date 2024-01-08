from rest_framework import serializers
 
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.Venta.serilizers import VentaSerializerPostRegistro
from apps.Suscripcion.serializers import SuscripcionSerializerPostRegistro
from apps.Frase.models import Frase
from apps.Frase.serializers import FraseSerializer, FraseSerializerPostRegistro

class DetalleSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSuscripcion
        fields = '__all__'

class DetalleSuscripcionSerializerPostRegistro(serializers.ModelSerializer):
    idVenta = VentaSerializerPostRegistro()
    idSuscripcion = SuscripcionSerializerPostRegistro()
    frase = serializers.SerializerMethodField()

    class Meta:
        model = DetalleSuscripcion
        fields = ['idVenta', 'fechaInicio', 'fechaFin', 'idSuscripcion', 'frase']

    def get_frase(self, obj):
        frase = Frase.objects.order_by('?').first()
        return FraseSerializerPostRegistro(frase).data['frase'] if frase else None
