from django.db import models
from apps.Cliente.models import Cliente
from apps.Users.models import User

# Create your models here.
class Registro(models.Model):
    idRegistro = models.AutoField(auto_created=True, primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):
        return "{}".format(self.idCliente.nombre+" - "+self.idUser.nombre)