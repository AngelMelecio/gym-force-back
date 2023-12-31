from django.db import models
from apps.Venta.models import Venta
from apps.Suscripcion.models import Suscripcion

# Create your models here.
class DetalleSuscripcion(models.Model):
    idSuscripcion = models.ForeignKey(Suscripcion, on_delete=models.DO_NOTHING)
    idVenta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
    fechaInicio = models.DateField(null=False, blank=False)
    fechaFin = models.DateField(null=False, blank=False)
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    descuento = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)

    def __str__(self):
        return "DetalleSuscripcion: %s %s %s %s %s %s" % (self.idSuscripcion, self.idVenta, self.fechaInicio, self.fechaFin, float(self.precioVenta), float(self.descuento))
