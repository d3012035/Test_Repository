# Generated by Django 4.1 on 2024-07-17 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0024_alter_carmodels_average_fuel_efficiency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodels',
            name='manufacturer',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='Edrive.manufacturers'),
        ),
    ]