# Generated by Django 4.1 on 2024-07-01 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0007_alter_users_driver_level_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carmodels',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='carmodels',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='ecodrivesites',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='ecodrivesites',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='fuelrecords',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='fuelrecords',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='manufacturers',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='manufacturers',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='mycars',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='mycars',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.AlterField(
            model_name='fuelrecords',
            name='fuel_efficiency',
            field=models.FloatField(editable=False),
        ),
        migrations.AlterField(
            model_name='mycars',
            name='target_fuel_efficiency',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
