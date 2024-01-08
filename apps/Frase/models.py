from django.db import models

class Frase(models.Model):
    idFrase = models.AutoField(auto_created=True, primary_key=True)
    frase = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.frase