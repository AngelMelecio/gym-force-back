# Generated by Django 3.1.7 on 2023-12-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0003_cliente_fotografia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='huella',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]