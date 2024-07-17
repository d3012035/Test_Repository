# custom_commands/management/commands/bulk_create_carmodels.py

from django.core.management.base import BaseCommand
from Edrive.models import CarModels

class Command(BaseCommand):
    help = 'Create initial car models and their average fuel efficiencies'

    def handle(self, *args, **kwargs):
        car_data = [
            {'car_model_name': 'AQUA', 'average_fuel_efficiency': 26.8},
            {'car_model_name': 'ROOMY', 'average_fuel_efficiency': 26.8},
            {'car_model_name': 'ALPHARD', 'average_fuel_efficiency': 17.4},
            {'car_model_name': 'RAIZE', 'average_fuel_efficiency': 27.0},
            {'car_model_name': 'N-BOX', 'average_fuel_efficiency': 27.8},
            {'car_model_name': 'FREED', 'average_fuel_efficiency': 24.5},
            {'car_model_name': 'VEZEL', 'average_fuel_efficiency': 24.8},
            {'car_model_name': 'CANBUS', 'average_fuel_efficiency': 27.9},
            {'car_model_name': 'Tanto', 'average_fuel_efficiency': 27.7},
            {'car_model_name': 'Rocky', 'average_fuel_efficiency': 27.0},
            {'car_model_name': 'NOTE', 'average_fuel_efficiency': 25.9},
            {'car_model_name': 'SERENA', 'average_fuel_efficiency': 21.1},
            {'car_model_name': 'DAYZ', 'average_fuel_efficiency': 28.1},
            {'car_model_name': 'X-TRAIL', 'average_fuel_efficiency': 21.5},
            
            # 他に必要なデータを追加
        ]

        # bulk_createを使ってデータを一括登録
        for data in car_data:
            car_model, created = CarModels.objects.update_or_create(
                car_model_name=data['car_model_name'],
                defaults={'average_fuel_efficiency': data['average_fuel_efficiency']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created {car_model}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'{car_model} already exists'))
        
        self.stdout.write(self.style.SUCCESS('Successfully created car models'))