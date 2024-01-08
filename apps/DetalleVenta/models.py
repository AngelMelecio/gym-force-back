from django.db import models

# Create your models here.
class DetalleVenta(models.Model):
    idVenta = models.ForeignKey('Venta.Venta', on_delete=models.DO_NOTHING)
    idProducto = models.ForeignKey('Producto.Producto', on_delete=models.DO_NOTHING)
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    cantidad = models.IntegerField(null=False, blank=False)
    descuento = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)

    def __str__(self):
        return "DetalleVenta: %s %s %s %s %s" % (self.idVenta, self.idProducto, self.precioVenta, self.cantidad, self.descuento)
