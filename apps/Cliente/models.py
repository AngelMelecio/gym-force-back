from django.db import models
from apps.AvailablePIN.models import AvailablePIN

def upload_to(instance, filename):
   return 'images/{filename}'.format(filename=filename)

class Cliente(models.Model):
    idCliente = models.AutoField(auto_created=True, primary_key=True)
    fotografia = models.ImageField(null=True, blank=True, upload_to=upload_to)
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    notas = models.CharField(max_length=1000, null=True, blank=True)
    huella = models.BinaryField(null=True, blank=True)
    pin = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.nombre+" "+self.apellidos)
    
    def get_full_name(self):
        if self:
            return f"{self.nombre} {self.apellidos}"
        return "---"

    def save(self, *args, **kwargs):
        if not self.pk and not self.pin:
            available_pin = AvailablePIN.objects.filter(isAssigned=False).first()
            if available_pin:
                self.pin = available_pin.pin
                available_pin.isAssigned = True
                available_pin.save()

        super(Cliente, self).save(*args, **kwargs)

