# Generated by Django 3.1.7 on 2023-09-23 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Suscripcion', '0001_initial'),
        ('Venta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleSuscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('precioVenta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(max_length=200)),
                ('idSuscripcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Suscripcion.suscripcion')),
                ('idVenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Venta.venta')),
            ],
        ),
    ]
