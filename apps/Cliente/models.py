from django.db import models

class Cliente(models.Model):
    idCliente = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    notas = models.CharField(max_length=1000, null=True, blank=True)
    huella = models.CharField(max_length=200,null=True, blank=True)
    pin = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.nombre+" "+self.apellidos)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.pin: 
            last_pin = Cliente.objects.all().order_by('-pin').first()
            if last_pin:
                self.pin = last_pin.pin + 1
            else:
                self.pin = 100

        super(Cliente, self).save(*args, **kwargs)

