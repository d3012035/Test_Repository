# Generated by Django 4.1 on 2024-07-19 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0031_rename_carmodels_carmodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='average_fuel_efficiency',
            field=models.FloatField(blank=True, null=True),
        ),
    ]