from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from apps.Frase.models import Frase
from apps.Frase.serializers import FraseSerializer

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def frase_api_view(request):
    if request.method == 'POST':
        pass
    if(request.method == 'GET'):
        pass

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def frase_detail_api_view(request, pk=None ):
     # Queryset
    frase = Frase.objects.filter( idFrase = pk ).first()
    
    # Validacion
    if frase:
        # Retrieve
        if request.method == 'GET':
            frase_s =  FraseSerializer(frase)
            return Response( frase_s.data, status=status.HTTP_200_OK )
        
    return Response(
        {'message':'No se encontró la frase'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
      