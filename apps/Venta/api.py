from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from apps.Venta.serilizers import VentaSerializer, VentaSerializerWithDetails
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

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def venta_api_view(request):
    if request.method == 'POST':
        
        # Substract data from the request
        productos = request.data.get('productos', [])
        suscripcion = request.data.get('suscripcion', None)
        id_clnt = request.data.get('cliente', None)
        id_usr = request.data.get('usuario', None)

        if not productos and suscripcion is None:
            return Response({"message":"Error de solicitud"}, status=status.HTTP_400_BAD_REQUEST)

        # Get total cost 
        total_cost = 0
        if len(productos) > 0:
            for p in productos:
                idP = p['idProducto']
                quantity = p['cantidad']
                prd = Producto.objects.filter(idProducto=idP).first()
                total_cost += float(prd.precio) * float(quantity)
                # Formation the products list
                p['precioVenta'] = prd.precio
                p['idProducto'] = prd


        if suscripcion:
            sus = Suscripcion.objects.filter(idSuscripcion=suscripcion['idSuscripcion']).first()
            total_cost += float(sus.precio)
       

        with transaction.atomic():
            cliente = Cliente.objects.filter(idCliente=id_clnt).first()
            usuario = User.objects.filter(id=id_usr).first()
            venta = Venta.objects.create(total=total_cost, idUser=usuario, idCliente=cliente)
            detalles_venta = [ 
                DetalleVenta(
                    idVenta = venta,
                    idProducto =  p['idProducto'],
                    cantidad = p['cantidad'] ,
                    precioVenta = p['precioVenta'],
                    descuento=0
                ) 
                for p in productos
            ]
            DetalleVenta.objects.bulk_create(detalles_venta)

            if suscripcion:
                DetalleSuscripcion.objects.create(
                    idSuscripcion = sus,
                    idVenta = venta,
                    fechaInicio = datetime.today().date(), 
                    fechaFin = datetime.today().date() + timedelta(days=sus.duracion),
                    precioVenta = sus.precio,   
                    descuento = 0,
                    estado = "activo"
                )
            
        vnt_srlzr = VentaSerializerWithDetails(venta)
        
        return Response(vnt_srlzr.data, status=status.HTTP_201_CREATED)

    if(request.method == 'GET'):
        pass

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def venta_detail_api_view(request, pk=None ):
    if request.method == 'GET':
        pass
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass