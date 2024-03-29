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
from apps.Registro.models import Registro
from apps.Users.models import User
from django.db import transaction
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from django.utils.timezone import make_aware
import pytz
from datetime import datetime, timedelta
import calendar
import pytz

def calcular_fecha_fin(fecha_inicio, duracion_meses):
    año = fecha_inicio.year
    mes = fecha_inicio.month + duracion_meses

    # Ajustar año y mes si mes > 12
    año += mes // 12
    mes = mes % 12 if mes % 12 != 0 else 12

    # Verificar la cantidad de días en el mes de destino
    dias_en_mes = calendar.monthrange(año, mes)[1]

    # Si el día de inicio existe en el mes de destino, usar ese día; 
    # de lo contrario, usar el último día del mes
    dia = fecha_inicio.day if fecha_inicio.day <= dias_en_mes else dias_en_mes

    fecha_fin = datetime(año, mes, dia).date()
    return fecha_fin


@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def venta_api_view(request):
    if request.method == 'POST':
        #Extraccion de datos de la request
        productos = request.data.get('productos', [])
        suscripcion = request.data.get('suscripcion', None)
        id_clnt = request.data.get('cliente', None)
        id_usr = request.data.get('usuario', None)

        #Validacion de datos de la request y recuperacion de los mismos en la DB
        total_cost = 0

        if not productos and suscripcion is None:
            return Response({"error": "Error de solicitud"}, status=status.HTTP_400_BAD_REQUEST)

        if suscripcion:
            sus = Suscripcion.objects.filter(idSuscripcion=suscripcion['idSuscripcion']).first()
            if not sus:
                return Response({"error": "Suscripción no encontrada."}, status=status.HTTP_400_BAD_REQUEST)

            total_cost += float(sus.precio)
        
        for p in productos:
            product=Producto.objects.filter(idProducto=p['idProducto']).first()
            if not product:
                return Response({"error": f"Producto con id {p['idProducto']} no encontrado."}, status=status.HTTP_400_BAD_REQUEST)
            total_cost += float(product.precio) * float(p['cantidad'])
        cliente = Cliente.objects.filter(idCliente=id_clnt).first()

        usuario = User.objects.filter(id=id_usr).first()
        if not usuario:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear venta, detalles de venta, detalles de suscripción y registro (der ser necesario)
        try:
            with transaction.atomic():
                venta = Venta.objects.create(total=total_cost, idUser=usuario, idCliente=cliente)

                #--- PRODUCTOS ---
                # Existencia e inventario de productos
                product_instances = []
                for p in productos:
                    # select_for_update() toma el valor que tiene el registro en la base de datos
                    # y no el que tiene en la memoria, esto para evitar que dos procesos
                    # tomen el mismo valor y se genere un error de concurrencia
                    prd = Producto.objects.select_for_update().filter(idProducto=p['idProducto']).first()
                    
                    # Validar que haya suficiente inventario
                    if prd.inventario < p['cantidad']:
                        raise ValidationError(f"No hay suficiente stock para el producto {prd.nombre}.")

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

                #--- SUSCRIPCION ---
                if suscripcion:
                    #Validamos si es necesario que tenga cliente asignado o no la suscripcion
                    if sus.duracion > 1 and not id_clnt:
                        raise ValidationError("Este tipo de suscripción debe tener un cliente asignado. Selecciona un cliente.")

                   #Ajustes generales
                    today = datetime.now().date()

                    if sus.duracion%30 == 0:
                        meses= int(sus.duracion/30)
                    else:
                        meses=0

                    #if sus.duracion == 1 and sus.tipo== 'Visita': sus.duracion = 0
    
                    detalle_suscripcion = DetalleSuscripcion.objects.filter(idVenta__idCliente=id_clnt).last()
                    
                    #Tiene historial de suscripciones
                    if detalle_suscripcion:
                        fecha_inicio = detalle_suscripcion.fechaFin
                        
                        #Tiene suscripcion activa
                        if (fecha_inicio - today).days >= 0: 
                            fecha_inicio = fecha_inicio 
                        #No tiene suscripcion activa
                        else:
                            fecha_inicio = today
                        
                        #Si la suscripcion es o no mensual
                        fecha_fin = calcular_fecha_fin(fecha_inicio, meses) if meses != 0 else fecha_inicio + timedelta(days=sus.duracion-1)

                    #No tiene historial de suscripciones
                    else :
                        fecha_inicio = today
                        
                        #Si la suscripcion es o no mensual
                        fecha_fin = calcular_fecha_fin(fecha_inicio, meses) if meses != 0 else fecha_inicio + timedelta(days=sus.duracion-1)
                    
                    DetalleSuscripcion.objects.create(
                        idSuscripcion=sus,
                        idVenta=venta,
                        fechaInicio=fecha_inicio,
                        fechaFin=fecha_fin ,
                        precioVenta=sus.precio,
                        descuento=0,
                    )
                    
                    #Crear ingreso de suscripcion visita con o sin cliente
                    idCliente = cliente if id_clnt else None
                    if(sus.tipo == 'Visita'):
                        Registro.objects.create(
                            idCliente=idCliente,
                            idUser=usuario,
                            fecha=today,
                        )
        except ValidationError as e:
            # e.detail es una lista o un diccionario de ErrorDetail
            # Si siempre es una lista y solo interesa el primer mensaje, podemos hacer:
            mensaje_error = e.detail[0] if e.detail else "Error desconocido"

            # Si e.detail es un diccionario y queremos concatenar todos los mensajes, podemos hacer:
            """
            if isinstance(e.detail, dict):
                mensajes = []
                for campo, errores in e.detail.items():
                    for error in errores:
                        mensajes.append(str(error))
                mensaje_error = '. '.join(mensajes)
            elif isinstance(e.detail, list):
                mensaje_error = ', '.join([str(error) for error in e.detail])
            """
            return Response({"error": mensaje_error}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": "Ocurrio un error inesperado, vuelva a intentarlo o contacte a los desarrolladores"}, status=status.HTTP_400_BAD_REQUEST)

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


    if inicio and fin:
        ventas = Venta.objects.filter(fecha__range=(inicio, fin)).order_by('fecha').reverse()
    else:
        ventas = Venta.objects.all().order_by('fecha').reverse()

    ventas_serializer = VentaSerializerWithDetails(ventas, many=True)
    return Response(ventas_serializer.data, status=status.HTTP_200_OK)