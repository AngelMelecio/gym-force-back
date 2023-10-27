from django.db import models
from apps.Cliente.models import Cliente
from apps.Users.models import User
# Create your models here.

class Venta(models.Model):
    idVenta = models.AutoField(auto_created=True, primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__ (self):
        return "{}".format(str(self.fecha)+" - "+str(self.total)+" - "+self.idCliente.nombre+" - "+self.idUser.nombre)
