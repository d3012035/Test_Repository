# Generated by Django 4.1 on 2024-08-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0032_alter_carmodel_average_fuel_efficiency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelrecord',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='fuelrecord',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
