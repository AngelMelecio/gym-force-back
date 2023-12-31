# Generated by Django 3.1.7 on 2024-01-06 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Suscripcion', '0005_auto_20231030_2253'),
        ('Venta', '0003_auto_20231219_2302'),
        ('DetalleSuscripcion', '0004_auto_20240104_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallesuscripcion',
            name='idSuscripcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Suscripcion.suscripcion'),
        ),
        migrations.AlterField(
            model_name='detallesuscripcion',
            name='idVenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Venta.venta'),
        ),
    ]
