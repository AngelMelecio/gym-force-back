from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from apps.Venta.serilizers import VentaSerializer, VentaSerializerWithDetails,VentaDetalleSerializerToReport
from apps.Venta.models import Venta
from apps.Producto.models import Producto
from apps.Producto.serializers import ProductoSerializer
from apps.Suscripcion.models import Suscripcion
from apps.Suscripcion.serializers import SuscripcionSerializer
from apps.DetalleVenta.models import DetalleVenta
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.Cliente.models import Cliente
from apps.Users.models import User
from django.db import transaction
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from django.utils.timezone import make_aware
import pytz



@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def venta_api_view(request):
    if request.method == 'POST':
        
        productos = request.data.get('productos', [])
        suscripcion = request.data.get('suscripcion', None)
        id_clnt = request.data.get('cliente', None)
        id_usr = request.data.get('usuario', None)

        if not productos and suscripcion is None:
            return Response({"message": "Error de solicitud"}, status=status.HTTP_400_BAD_REQUEST)

        total_cost = 0

        if suscripcion:
            sus = Suscripcion.objects.filter(idSuscripcion=suscripcion['idSuscripcion']).first()
            if not sus:
                raise ValidationError("Suscripción no encontrada.")
            total_cost += float(sus.precio)
        
        for p in productos:
            product=Producto.objects.filter(idProducto=p['idProducto']).first()
            if not product:
                raise ValidationError("Producto no encontrado.")
            total_cost += float(product.precio) * float(p['cantidad'])

        cliente = Cliente.objects.filter(idCliente=id_clnt).first()
        if not cliente:
            raise ValidationError("Cliente no encontrado.")

        usuario = User.objects.filter(id=id_usr).first()
        if not usuario:
            raise ValidationError("Usuario no encontrado.")

        try:
            with transaction.atomic():
                venta = Venta.objects.create(total=total_cost, idUser=usuario, idCliente=cliente)
                
                 # Existencia e inventario de productos
                product_instances = []
                for p in productos:
                    # select_for_update() toma el valor que tiene el registro en la base de datos
                    # y no el que tiene en la memoria, esto para evitar que dos procesos
                    # tomen el mismo valor y se genere un error de concurrencia
                    prd = Producto.objects.select_for_update().filter(idProducto=p['idProducto']).first()
                    
                    if not prd:
                        raise ValidationError(f"Producto con id {p['idProducto']} no encontrado.")
                    
                    # Validar que haya suficiente inventario
                    if prd.inventario < p['cantidad']:
                        raise ValidationError(f"No hay suficiente stock para el producto {prd.nombre}.")

                    total_cost += float(prd.precio) * float(p['cantidad'])
                    p['precioVenta'] = prd.precio
                    p['idProducto'] = prd
                    product_instances.append(prd)

                detalles_venta = [ 
                    DetalleVenta(
                        idVenta = venta,
                        idProducto =  p['idProducto'],
                        cantidad = p['cantidad'],
                        precioVenta = p['precioVenta'],
                        descuento=0
                    ) 
                    for p in productos
                ]
                DetalleVenta.objects.bulk_create(detalles_venta)

                # Actualizar inventario
                for prd, p in zip(product_instances, productos):
                    prd.inventario -= p['cantidad']
                    prd.save()

                if suscripcion:
                    fecha_fin = datetime.now(pytz.timezone('America/Mexico_City')).date() + timedelta(days=sus.duracion)

                    DetalleSuscripcion.objects.create(
                        idSuscripcion=sus,
                        idVenta=venta,
                        fechaInicio=datetime.now(pytz.timezone('America/Mexico_City')).date(),
                        fechaFin=fecha_fin ,
                        precioVenta=sus.precio,
                        descuento=0,
                    )
            
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vnt_srlzr = VentaSerializerWithDetails(venta)
        return Response(vnt_srlzr.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def reporte_ventas_api_view(request,fecha_inicio, fecha_fin):

    # Conversión de las cadenas de fecha a objetos datetime
    format_str = '%Y-%m-%d'  # El formato en que se espera la fecha
    inicio = make_aware(datetime.strptime(fecha_inicio, format_str))
    fin = make_aware(datetime.strptime(fecha_fin, format_str))

    # Ajustar fin para incluir todo el día
    fin += timedelta(days=1) - timedelta(seconds=1)
    print(fin)

    if inicio and fin:
        ventas = Venta.objects.filter(fecha__range=(inicio, fin))
    else:
        ventas = Venta.objects.all()

    ventas_serializer = VentaDetalleSerializerToReport(ventas, many=True)
    return Response(ventas_serializer.data, status=status.HTTP_200_OK)