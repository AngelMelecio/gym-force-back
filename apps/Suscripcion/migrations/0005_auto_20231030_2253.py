# Generated by Django 3.1.7 on 2023-10-31 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Suscripcion', '0004_auto_20231030_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suscripcion',
            name='nombre',
        ),
        migrations.AddField(
            model_name='suscripcion',
            name='tipo',
            field=models.CharField(choices=[('Visita', 'Visita'), ('Semana', 'Semana'), ('Mensualidad', 'Mensualidad'), ('Trimestre', 'Trimestre'), ('Semestre', 'Semestre'), ('Anualidad', 'Anualidad')], default='Mensualidad', max_length=20),
        ),
    ]