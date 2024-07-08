from django.contrib import admin
from .models import Manufacturers, CarModels, Users, MyCars, FuelRecords, EcoDriveSites

admin.site.register(Manufacturers)
admin.site.register(CarModels)
admin.site.register(Users)
admin.site.register(MyCars)
admin.site.register(FuelRecords)
admin.site.register(EcoDriveSites)

# Register your models here.
