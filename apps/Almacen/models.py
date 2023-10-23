from django.db import models

class Almacen(models.Model):
    idAlmacen = models.AutoField(auto_created=True, primary_key=True)
    