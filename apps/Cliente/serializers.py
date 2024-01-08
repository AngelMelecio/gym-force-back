from rest_framework import serializers
from apps.Cliente.models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
    
    def update(self, instance, validated_data):
        # Handle the file separately if it's in the request
        huella_file = self.context['request'].FILES.get('huella')
        print(huella_file)
        if huella_file:
            instance.huella = huella_file.read()

        # Handle other fields normally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class ClienteSerializerPostRegistro(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre','apellidos','idCliente','fotografia']


class ClienteRegistrosSerializer(serializers.ModelSerializer):
    hasHuella = serializers.SerializerMethodField('get_hasHuella')
    class Meta:
        model = Cliente
        fields = ['idCliente','nombre','apellidos','hasHuella']

    def get_hasHuella(self, obj):
        return obj.huella is not None