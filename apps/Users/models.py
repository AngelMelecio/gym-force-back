from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

class UserManager(BaseUserManager):
    def _create_user(self, nombre, apellidos, fotografia ,correo, usuario, password, is_staff, is_superuser, rol,**extra_fields):
        user = self.model(
            nombre = nombre,
            apellidos= apellidos,
            fotografia = fotografia,
            correo = correo,
            usuario = usuario,
            is_staff = is_staff,
            is_superuser = is_superuser,
            rol = rol,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,nombre,apellidos,fotografia, correo, usuario ,rol, password=None, **extra_fields):
        return self._create_user(nombre,apellidos,fotografia, correo, usuario, rol, password, False, False, **extra_fields)

    def create_superuser(self,nombre,apellidos, fotografia, correo, usuario, password=None, **extra_fields):
        return self._create_user(nombre, apellidos, fotografia, correo, usuario, password, True, True,'Administrador', **extra_fields)

    
def upload_to(instance, filename):
   return 'images/{filename}'.format(filename=filename)
  
class User(AbstractBaseUser,PermissionsMixin):
    nombre = models.CharField('Nombres', max_length=100, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=100, blank=True, null=True)
    fotografia = models.ImageField(null=True, blank=True, upload_to=upload_to)
    correo = models.EmailField('Correo Electrónico',max_length=200, unique=True, null=True)
    usuario = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    rol = models.CharField(max_length=20,
                            choices=[('Empleado', 'Empleado'),
                                     ('Administrador', 'Administrador')],
                            default='Empleado')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombre','apellidos','correo']

    objects = UserManager()

    def __str__(self):
        return f'{self.usuario}'