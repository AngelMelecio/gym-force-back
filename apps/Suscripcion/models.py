from django.db import models

# Create your models here.

class Suscripcion(models.Model):
    idSuscripcion = models.AutoField(auto_created=True, primary_key=True)
    tipo = models.CharField(max_length=20,
                            choices=[('Visita', 'Visita'),
                                     ('Semana', 'Semana'),
                                     ('Mensualidad', 'Mensualidad'),
                                     ('Trimestre', 'Trimestre'),
                                     ('Semestre', 'Semestre'),
                                     ('Anualidad', 'Anualidad')],
                            default='Mensualidad')
    descripcion = models.CharField(max_length=1000, null=True, blank=True)
    modalidad = models.CharField(max_length=20,
                            choices=[('Gym', 'Gym'),
                                     ('Spin', 'Spin'),
                                     ('Yoga', 'Yoga'),
                                     ('Gym + Spin', 'Gym + Spin'),
                                     ('Gym + Yoga', 'Gym + Yoga'),
                                     ('Gym + Spin + Yoga', 'Gym + Spin + Yoga')],
                            default='Gym')
    duracion = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)    
    icono = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.tipo +" "+ self.modalidad+ " - " + str(self.duracion) + " días / $" + str(self.precio) ) 
    
    def get_nombre(self):
        return "{}".format(self.tipo +" "+ self.modalidad)