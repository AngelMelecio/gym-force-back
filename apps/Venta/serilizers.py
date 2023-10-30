from rest_framework import serializers
 
from apps.Venta.models import Venta
from apps.DetalleVenta.models import DetalleVenta
from apps.Cliente.serializers import ClienteSerializerPostRegistro
from apps.Users.serializer import SimpleUserSerializer
from apps.DetalleSuscripcion.models import DetalleSuscripcion

class DetallesVentaSerializer(serializers.ModelSerializer):
    nombreProducto = serializers.ReadOnlyField(source='idProducto.nombre')
    class Meta:
        model = DetalleVenta
        fields = ['nombreProducto', 'precioVenta','cantidad']

class DetallesSuscripcionSerializer(serializers.ModelSerializer):
    nombreSuscripcion = serializers.ReadOnlyField(source='idSuscripcion.nombre')
    precio = serializers.ReadOnlyField(source='idSuscripcion.precio')
    class Meta:
        model = DetalleSuscripcion
        fields = ['nombreSuscripcion','fechaFin']


class VentaSerializerWithDetails(serializers.ModelSerializer):
    detallesVenta = DetallesVentaSerializer(source='detalleventa_set', many=True, read_only=True)
    detallesSuscripcion = DetallesSuscripcionSerializer(source='detallesuscripcion_set', many=True, read_only=True)
    
    cliente = serializers.ReadOnlyField( source='idCliente.get_full_name' )
    usuario = serializers.ReadOnlyField( source='idUser.get_full_name' )

    class Meta:
        model = Venta
        fields = ['detallesVenta','detallesSuscripcion','cliente','usuario','fecha','idVenta','total'] 

    
class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class VentaSerializerPostRegistro(serializers.ModelSerializer):
    idCliente = ClienteSerializerPostRegistro()
    class Meta:
        model = Venta
        fields = ['idCliente']