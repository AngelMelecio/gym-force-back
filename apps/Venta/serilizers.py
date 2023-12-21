from rest_framework import serializers
 
from apps.Venta.models import Venta
from apps.DetalleVenta.models import DetalleVenta
from apps.Cliente.serializers import ClienteSerializerPostRegistro
from apps.Users.serializer import SimpleUserSerializer
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.Producto.models import Producto
from apps.Suscripcion.models import Suscripcion

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre','precio']

class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = ['nombre','precio']

class DetallesVentaSerializer(serializers.ModelSerializer):
    nombreProducto = serializers.ReadOnlyField(source='idProducto.nombre')
    class Meta:
        model = DetalleVenta
        fields = ['nombreProducto', 'precioVenta','cantidad']

class DetallesSuscripcionSerializer(serializers.ModelSerializer):
    nombreSuscripcion = serializers.ReadOnlyField(source='idSuscripcion.get_nombre')
    precio = serializers.ReadOnlyField(source='idSuscripcion.precio')
    class Meta:
        model = DetalleSuscripcion
        fields = ['nombreSuscripcion','precio','fechaFin']


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

class VentaDetalleSerializerToReport(serializers.ModelSerializer):
    nombre_usuario = serializers.CharField(source='idUser.get_full_name')
    nombre_cliente = serializers.CharField(source='idCliente.get_full_name')
    detalles = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['fecha', 'total', 'nombre_usuario', 'nombre_cliente', 'detalles']

    def get_detalles(self, obj):
        detalles_venta = DetalleVenta.objects.filter(idVenta=obj)
        detalles_suscripcion = DetalleSuscripcion.objects.filter(idVenta=obj)
        detalles = []

        for detalle in detalles_venta:
            producto = Producto.objects.get(idProducto=detalle.idProducto.idProducto)
            detalles.append({
                'tipo': 'Producto',
                'nombre': producto.nombre,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precioVenta,
                'importe': detalle.cantidad * detalle.precioVenta
            })

        for detalle in detalles_suscripcion:
            suscripcion = Suscripcion.objects.get(idSuscripcion=detalle.idSuscripcion.idSuscripcion)
            detalles.append({
                'tipo': 'Suscripcion',
                'nombre': suscripcion.get_nombre(),
                'cantidad': 1,  # Asumiendo una suscripción por venta
                'precio_unitario': detalle.precioVenta,
                'importe': detalle.precioVenta
            })

        return detalles