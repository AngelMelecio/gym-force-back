from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from apps.Cliente.models import Cliente
from apps.Cliente.serializers import ClienteSerializerPostRegistro
from apps.Registro.models import Registro
from apps.Registro.serializers import RegistroSerializer, RegistroSerializerToReport
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.DetalleSuscripcion.serializers import DetalleSuscripcionSerializerPostRegistro
from apps.Users.models import User
from datetime import datetime
from django.utils.timezone import make_aware
from datetime import timedelta
import pytz
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def registro_api_view(request):
    if request.method == 'POST':
        
        # Verificar el PIN
        req_pin = request.data.get('pin')
        req_id = request.data.get('idCliente')
        isFingerprint = request.data.get('isFingerprint')

        if req_id:
            cliente = Cliente.objects.filter(idCliente=req_id).first()
        elif req_pin and req_pin.isdigit():
            cliente = Cliente.objects.filter(pin=req_pin).first()
        else:
            return Response({"message": "PIN no válido"}, status=status.HTTP_400_BAD_REQUEST)

        # Current date in the appropriate timezone
        today = datetime.now(pytz.timezone('America/Mexico_City')).date()
        
        if cliente:
            detalle = DetalleSuscripcion.objects.filter(idVenta__idCliente=cliente.idCliente).last()
            usuario = User.objects.filter(id=request.data.get('idUser')).first()

            if not detalle:
                return Response({'message': 'Cliente sin suscripción'}, status=status.HTTP_404_NOT_FOUND)

            dll_sus_srlzr = DetalleSuscripcionSerializerPostRegistro(detalle)
            fecha_fin = detalle.fechaFin

            if fecha_fin.date() >= today:
                # Create the record
                registro = Registro(idCliente=cliente, idUser=usuario)
                try:
                    registro.save()
                    
                    print('Registro guardado')
                    
                    print('Is fingerprint: ', isFingerprint)
                    if isFingerprint is True:
                        channels_layer = get_channel_layer()
                        async_to_sync(channels_layer.group_send)(
                            'access_socket', # Channel group name
                            {   
                                'type':'accessStatus', # Consumer method
                                'data': dll_sus_srlzr.data
                            }
                        )
                    
                    print('Propagado por websocket')
                    return Response({
                        'message': 'Registro exitoso',
                        'registro': dll_sus_srlzr.data
                    }, status=status.HTTP_200_OK)

                    # if isFingerprint: propagate through websocket

                except Exception as e:
                    # Handle save error
                    return Response({'message': f'Error al guardar el registro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'message': 'Suscripción vencida', 'registro': dll_sus_srlzr.data}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'message': 'Cliente No encontrado'}, status=status.HTTP_404_NOT_FOUND)


    if(request.method == 'GET'):
        pass

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def registro_detail_api_view(request, pk=None, sus=None ):
    if request.method == 'GET':
        detalle = DetalleSuscripcion.objects.filter(id=sus).first()
        registros = Registro.objects.filter(idCliente=pk).filter(fecha__range=[detalle.fechaInicio, detalle.fechaFin])
        registro_serializer = RegistroSerializer(registros, many=True)
        return Response(registro_serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT': 
        pass
    if request.method == 'DELETE':
        pass

@api_view(['GET'])
def registros_api_view(request, fecha_inicio, fecha_fin):
    
    # Conversión de las cadenas de fecha a objetos datetime
    format_str = '%Y-%m-%d'  # El formato en que se espera la fecha
    inicio = make_aware(datetime.strptime(fecha_inicio, format_str))
    fin = make_aware(datetime.strptime(fecha_fin, format_str))

    # Ajustar fin para incluir todo el día
    fin += timedelta(days=1) - timedelta(seconds=1)

    if inicio and fin:
        registros = Registro.objects.filter(fecha__range=(inicio, fin))
    else:
        registros = Registro.objects.all()
    registros_serializer = RegistroSerializerToReport(registros, many=True)
    return Response(registros_serializer.data, status=status.HTTP_200_OK)
         

    