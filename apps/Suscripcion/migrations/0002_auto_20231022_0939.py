# Generated by Django 3.1.7 on 2023-10-22 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Suscripcion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suscripcion',
            name='categoria',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]