from django.db import models
from apps.Cliente.models import Cliente
from apps.Users.models import User
# Create your models here.

class Venta(models.Model):
    idVenta = models.AutoField(auto_created=True, primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, blank=True, null=True)
    idUser = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__ (self):
        nombre_cliente = ""
        if self.idCliente: 
            nombre_cliente = self.idCliente.get_full_name()
        return "{}".format(
            str(self.fecha) + " - " + 
            str(self.total) + " - " + 
            nombre_cliente + " - " + 
            self.idUser.nombre )
