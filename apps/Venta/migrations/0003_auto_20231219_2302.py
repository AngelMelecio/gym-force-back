# Generated by Django 3.1.7 on 2023-12-20 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0002_auto_20231029_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
