# Generated by Django 4.1 on 2024-06-30 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0006_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='driver_level',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='users',
            name='target_achievement_count',
            field=models.IntegerField(default=0),
        ),
    ]
