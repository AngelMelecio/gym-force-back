from django.db import models

# Create your models here.

class Producto(models.Model):
    idProducto = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)    
    inventario = models.IntegerField()

    def __str__(self):
        return "{}".format(self.nombre+" - $"+self.precio+" / "+self.inventario+" unidades")
