# Generated by Django 3.1.7 on 2023-10-23 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='pin',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='huella',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
