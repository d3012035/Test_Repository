# Generated by Django 4.1 on 2024-07-10 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0017_alter_mycars_next_inspection_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycars',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Edrive.carmodels'),
        ),
        migrations.AlterField(
            model_name='mycars',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mycars', to=settings.AUTH_USER_MODEL),
        ),
    ]
