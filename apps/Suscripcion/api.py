from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

from apps.Suscripcion.models import Suscripcion
from apps.Suscripcion.serializers import SuscripcionSerializer

from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def suscripcion_api_view(request):
    # list
    if request.method == 'GET':
        suscripcion = Suscripcion.objects.all()
        suscripcion_serializer = SuscripcionSerializer(suscripcion,many=True)
        return Response( suscripcion_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        suscripcion_serializer = SuscripcionSerializer(data=request.data)
        if suscripcion_serializer.is_valid():
            suscripcion_serializer.save()
            return Response( {'message':'Suscripcion creada correctamente!'}, status=status.HTTP_201_CREATED )
        return Response( suscripcion_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def suscripcion_detail_api_view(request, pk=None ):
    # Queryset
    suscripcion = Suscripcion.objects.filter( idSuscripcion = pk ).first()
    
    # Validacion
    if suscripcion:
        # Retrieve
        if request.method == 'GET':
            suscripcion_serializer =  SuscripcionSerializer(suscripcion)
            return Response( suscripcion_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            suscripcion_serializer = SuscripcionSerializer(suscripcion, data = request.data)
            if suscripcion_serializer.is_valid():
                suscripcion_serializer.save()
                return Response( {'message':'Suscripcion actualizada correctamente!'}, status=status.HTTP_200_OK)
            return Response(suscripcion_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            suscripcion = Suscripcion.objects.filter( idSuscripcion = pk ).first()
            try:
                suscripcion.delete()
                return Response(
                    {'message':'Suscripcion eliminada correctamente!'}, 
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'message':'¡No es posible eliminar un Suscripcion en uso!'}, 
                    status=status.HTTP_409_CONFLICT
                )

    return Response(
        {'message':'No se encontró el Suscripcion'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
      