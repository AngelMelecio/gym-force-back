from django.db import models

# Create your models here.

class Cliente(models.Model):
    idCliente = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    notas = models.CharField(max_length=1000, null=True, blank=True)
    huella = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.nombre+" "+self.apellidos)

