from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

from apps.DetalleSuscripcion.models import DetalleSuscripcion
from apps.DetalleSuscripcion.serializers import DetalleSuscripcionSerializer

from rest_framework.parsers import MultiPartParser, JSONParser


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
        elif request.method == 'PUT':
            ds_srlzr = DetalleSuscripcionSerializer(ds, data = request.data, partial=True)
            if ds_srlzr.is_valid():
                ds_srlzr.save()
                return Response( {'message':'Se aplazó correctamente!'}, status=status.HTTP_200_OK)
            return Response(ds_srlzr.errors, status = status.HTTP_400_BAD_REQUEST)

    return Response(
        {'message':'No se encontró el detalle de la suscripcion'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
      