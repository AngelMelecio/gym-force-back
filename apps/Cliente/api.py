from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Cliente.models import Cliente
from apps.Cliente.serializers import ClienteSerializer, ClienteRegistrosSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from datetime import datetime, timedelta
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.Venta.models import Venta
from apps.Suscripcion.models import Suscripcion
import pytz


def get_info_adicional_cliente(cliente):
    # Obtenemos la venta más reciente del cliente
    detalle_suscripcion = DetalleSuscripcion.objects.filter(
        idVenta__idCliente=cliente.data.get('idCliente')
    ).last()

    if detalle_suscripcion:
        # Utilizamos datetime.now() sin zona horaria
        today = datetime.now().date()

        # Calculamos la diferencia de días
        diferencia_dias = (detalle_suscripcion.fechaFin - today).days

        # Construimos la información de la suscripción
        suscripcion = detalle_suscripcion.idSuscripcion
        suscripcion = f"{suscripcion.tipo} {suscripcion.modalidad}"
    else:
        diferencia_dias = None
        suscripcion = ""

    return {
        "diferencia_dias": diferencia_dias,
        "suscripcion": suscripcion
    }


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, JSONParser])
def cliente_api_view(request):
    # list
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        response_data = []

        for cliente in clientes:
            cliente_serializer = ClienteSerializer(cliente)

            info_adicional = get_info_adicional_cliente(cliente_serializer)

            # Serializamos los datos del cliente
            cliente_data = cliente_serializer.data
            cliente_data["diferencia_dias"] = info_adicional["diferencia_dias"]
            cliente_data["suscripcion"] = info_adicional["suscripcion"]

            response_data.append(cliente_data)

        return Response(response_data, status=status.HTTP_200_OK)
    # Create
    elif request.method == 'POST':
        cliente_serializer = ClienteSerializer(data=request.data)
        if cliente_serializer.is_valid():
            cliente_serializer.save()
            return Response({'message': '¡Cliente creado correctamente!',
                             'idCliente': cliente_serializer.data['idCliente']
                             }, status=status.HTTP_201_CREATED)
        return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def cliente_detail_api_view(request, pk=None):
    # Queryset
    cliente = Cliente.objects.filter(idCliente=pk).first()

    # Validacion
    if cliente:
        # Retrieve
        if request.method == 'GET':
            cliente_serializer = ClienteSerializer(cliente)
            info_dias = get_info_adicional_cliente(cliente_serializer)
            
            historico_suscripciones = []
           
            detalles_suscripcion = DetalleSuscripcion.objects.filter(idVenta__idCliente=cliente_serializer.data['idCliente'])
            for detalle in detalles_suscripcion:
                suscripcion_data = {
                    "id_suscripcion": detalle.idSuscripcion.idSuscripcion,
                    "id_detalle_suscripcion": detalle.id,
                    "nombre_suscripcion": f"{detalle.idSuscripcion.tipo} {detalle.idSuscripcion.modalidad}",
                    "fecha_inicio": detalle.fechaInicio,
                    "fecha_fin": detalle.fechaFin
                }
                historico_suscripciones.append(suscripcion_data)

            historico_suscripciones.sort(key=lambda x: x['fecha_fin'], reverse=True)

            response_data = cliente_serializer.data
            response_data["diferencia_dias"] = info_dias["diferencia_dias"]
            response_data["suscripcion"] = info_dias["suscripcion"]
            response_data["historico_suscripciones"] = historico_suscripciones

            return Response(response_data, status=status.HTTP_200_OK)

        # Update
        elif request.method == 'PUT':
            cliente_serializer = ClienteSerializer(
                cliente, 
                data=request.data, 
                partial = True, 
                context={'request': request}
            )
            if cliente_serializer.is_valid():
                cliente_serializer.save()
                return Response({'message': '¡Cliente actualizado correctamente!'}, 
                                status=status.HTTP_200_OK)
            return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Delete
        elif request.method == 'DELETE':
            cliente = Cliente.objects.filter(idCliente=pk).first()
            try:
                cliente.delete()
                return Response(
                    {'message': '¡Cliente eliminado correctamente!'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'message': '¡No es posible eliminar un Cliente en uso!'},
                    status=status.HTTP_409_CONFLICT
                )

    return Response(
        {'message': 'No se encontró el Cliente'},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def clientes_registrar_api_view(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        cliente_serializer = ClienteRegistrosSerializer(clientes, many=True)
        return Response(cliente_serializer.data, status=status.HTTP_200_OK)
 