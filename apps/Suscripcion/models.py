from django.db import models

# Create your models here.

class Suscripcion(models.Model):
    idSuscripcion = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000, null=True, blank=True)
    categoria = models.CharField(max_length=200,null=True, blank=True)
    duracion = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)    
    icono = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return "{}".format( self.nombre + " - " + str(self.duracion) + " días / $" + str(self.precio) ) 