# Generated by Django 4.1 on 2024-07-10 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0018_alter_mycars_car_model_alter_mycars_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycars',
            name='car_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Edrive.carmodels'),
        ),
    ]
