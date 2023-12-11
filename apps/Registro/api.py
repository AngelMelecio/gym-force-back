from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from apps.Cliente.models import Cliente
from apps.Cliente.serializers import ClienteSerializerPostRegistro
from apps.Registro.models import Registro
from apps.Registro.serializers import RegistroSerializer
from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.DetalleSuscripcion.serializers import DetalleSuscripcionSerializerPostRegistro
from datetime import datetime

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def registro_api_view(request):
    if request.method == 'POST':
        
        # Verificar el PIN
        req_pin = request.data.get('pin')
        if not req_pin or not req_pin.isdigit():
            return Response({"message": "PIN no valido"}, status=status.HTTP_400_BAD_REQUEST)
       
        # Datos del cliente del request
        cliente = Cliente.objects.filter(pin=req_pin).first()
        if cliente :
            cl_srlzr = ClienteSerializerPostRegistro(cliente)
            id_cliente = cl_srlzr.data.get('idCliente')

            # Obtener detalles de la suscripcion del cliente
            query = DetalleSuscripcion.objects.filter( idVenta__idCliente=id_cliente ).first()
            dll_sus_srlzr = DetalleSuscripcionSerializerPostRegistro( query )

            # Compara fecha de fin con fecha actual
            fecha_fin = datetime.strptime(dll_sus_srlzr.data.get('fechaFin'), '%Y-%m-%d').date()
            today = datetime.today().date()

            if fecha_fin >= today:    
                # Crear el registro de entrada
                rgt = {
                    "estado": "TODO",
                    "idCliente": id_cliente,
                    "idUser": request.data.get('idUser')
                }
                rgt_srlzr = RegistroSerializer(data=rgt)
                if rgt_srlzr.is_valid():
                    rgt_srlzr.save()
                    return Response( {
                        'message':'Registro exitoso',
                        'registro':dll_sus_srlzr.data    
                    }, status=status.HTTP_200_OK )

            else:
                return Response( {
                    'message':'Suscripción vencida',
                    'registro':dll_sus_srlzr.data
                    }, status=status.HTTP_409_CONFLICT )
        else:
            return Response( {'message':'Cliente No encontrado'}, status=status.HTTP_404_NOT_FOUND )



    if(request.method == 'GET'):
        pass

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def registro_detail_api_view(request, pk=None ):
    if request.method == 'GET':
        registros = Registro.objects.filter(idCliente=pk)
        registro_serializer = RegistroSerializer(registros, many=True)
        return Response(registro_serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT': 
        pass
    if request.method == 'DELETE':
        pass

    