# Generated by Django 4.1 on 2024-06-28 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edrive', '0004_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcoDriveSites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('ecodrive_url', models.CharField(max_length=260)),
                ('site_title', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'eco_drive_sites',
            },
        ),
        migrations.AddField(
            model_name='carmodels',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Edrive.manufacturers'),
        ),
    ]
