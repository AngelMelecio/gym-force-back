from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

from apps.Producto.models import Producto
from apps.Producto.serializers import ProductoSerializer

from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def producto_api_view(request):
    # list
    if request.method == 'GET':
        producto = Producto.objects.all()
        producto_serializer = ProductoSerializer(producto,many=True)
        return Response( producto_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        producto_serializer = ProductoSerializer(data=request.data)
        if producto_serializer.is_valid():
            producto_serializer.save()
            return Response( {'message':'Producto creado correctamente!'}, status=status.HTTP_201_CREATED )
        return Response( producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def producto_detail_api_view(request, pk=None ):
    # Queryset
    producto = Producto.objects.filter( idProducto = pk ).first()
    
    # Validacion
    if producto:
        # Retrieve
        if request.method == 'GET':
            producto_serializer =  ProductoSerializer(producto)
            return Response( producto_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            producto_serializer = ProductoSerializer(producto, data = request.data)
            if producto_serializer.is_valid():
                producto_serializer.save()
                return Response( {'message':'Producto actualizado correctamente!'}, status=status.HTTP_200_OK)
            return Response(producto_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            producto = Producto.objects.filter( idProducto = pk ).first()
            try:
                Producto.delete()
                return Response(
                    {'message':'Producto eliminado correctamente!'}, 
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'message':'¡No es posible eliminar un producto en uso!'}, 
                    status=status.HTTP_409_CONFLICT
                )

    return Response(
        {'message':'No se encontró el producto'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
      