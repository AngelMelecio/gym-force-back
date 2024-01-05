from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.DetalleSuscripcion.serializers import DetalleSuscripcionSerializer

from rest_framework.parsers import MultiPartParser, JSONParser

from datetime import datetime


@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def ds_change_date_end_api_view(request, pk=None ):
    # Queryset
    ds = DetalleSuscripcion.objects.filter( id = pk ).first()
    print(request.data)
    # Validacion
    if ds:
        # Retrieve
        if request.method == 'GET':
            ds_srlzr =  DetalleSuscripcionSerializer(ds)
            return Response( ds_srlzr.data, status=status.HTTP_200_OK )
        
        # Update
       # Inside your PUT request handling
        elif request.method == 'PUT':
            # Copy request.data to a mutable dictionary
            updated_data = request.data.copy()

            if 'fechaFin' in updated_data:
                try:
                    fecha_fin_str = updated_data['fechaFin']
                    # Assuming that the time part is not important and by default to midnight
                    
                    updated_data['fechaFin'] = fecha_fin_str
                except ValueError:
                    # Handle the error if the date format is incorrect
                    return Response({'message': 'Fecha incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

            ds_srlzr = DetalleSuscripcionSerializer(ds, data=updated_data, partial=True)
            if ds_srlzr.is_valid():
                ds_srlzr.save()
                return Response({'message': 'Se aplazó correctamente!'}, status=status.HTTP_200_OK)
            return Response(ds_srlzr.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {'message':'No se encontró el detalle de la suscripcion'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
      