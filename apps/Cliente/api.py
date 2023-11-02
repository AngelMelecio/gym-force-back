from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Cliente.models import Cliente
from apps.Cliente.serializers import ClienteSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def cliente_api_view(request):
    # list
    if request.method == 'GET':
        cliente = Cliente.objects.all()
        cliente_serializer = ClienteSerializer(cliente,many=True)
        return Response( cliente_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        cliente_serializer = ClienteSerializer(data=request.data)
        if cliente_serializer.is_valid():
            cliente_serializer.save()
            return Response( {'message':'¡Cliente creado correctamente!',
                              'idCliente':cliente_serializer.data['idCliente']
                              }, status=status.HTTP_201_CREATED )
        return Response( cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def cliente_detail_api_view(request, pk=None ):
    # Queryset
    cliente = Cliente.objects.filter( idCliente = pk ).first()
    
    # Validacion
    if cliente:
        # Retrieve
        if request.method == 'GET':
            cliente_serializer =  ClienteSerializer(cliente)
            return Response( cliente_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            cliente_serializer = ClienteSerializer(cliente, data = request.data)
            if cliente_serializer.is_valid():
                cliente_serializer.save()
                return Response( {'message':'¡Cliente actualizado correctamente!'}, status=status.HTTP_200_OK)
            return Response(cliente_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            cliente = Cliente.objects.filter( idCliente = pk ).first()
            try:
                cliente.delete()
                return Response(
                    {'message':'¡Cliente eliminado correctamente!'}, 
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'message':'¡No es posible eliminar un Cliente en uso!'}, 
                    status=status.HTTP_409_CONFLICT
                )

    return Response(
        {'message':'No se encontró el Cliente'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
        