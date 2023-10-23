from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def appname_api_view(request):
    if request.method == 'POST':
        pass
    if(request.method == 'GET'):
        pass

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def appname_detail_api_view(request, pk=None ):
    if request.method == 'GET':
        pass
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass