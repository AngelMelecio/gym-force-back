# Generated by Django 3.1.7 on 2023-12-26 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvailablePIN',
            fields=[
                ('idAvailablePIN', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('pin', models.IntegerField(unique=True)),
                ('isAssigned', models.BooleanField(default=False)),
            ],
        ),
    ]
