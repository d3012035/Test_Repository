# Generated by Django 4.1 on 2024-07-17 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0022_alter_user_licence_expiry_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodels',
            name='car_group',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
