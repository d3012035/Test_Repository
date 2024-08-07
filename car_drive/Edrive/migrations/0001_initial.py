# Generated by Django 4.1 on 2024-06-23 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('user_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('licence_expiry_on', models.DateField()),
                ('driver_level', models.IntegerField()),
                ('target_acivement_count', models.IntegerField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
