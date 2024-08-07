# Generated by Django 4.1 on 2024-06-27 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0002_carmodels_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('manufacturer_name', models.CharField(max_length=70)),
            ],
            options={
                'db_table': 'manufacturers',
            },
        ),
    ]
