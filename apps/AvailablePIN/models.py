from django.db import models

class AvailablePIN(models.Model):
    idAvailablePIN = models.AutoField(auto_created=True, primary_key=True)
    pin = models.IntegerField(unique=True)
    isAssigned = models.BooleanField(default=False)
    
    def __str__(self):
        return "{}".format(self.pin)
    