from rest_framework import serializers
 
from apps.Appname.models import Appname
 

class AppnameSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Appname
        fields = '__all__'