from django.contrib import admin
from .models import Manufacturers, CarModels,MyCars, FuelRecords, EcoDriveSites
from .models import User

admin.site.register(Manufacturers)
admin.site.register(CarModels)
admin.site.register(MyCars)
admin.site.register(FuelRecords)
admin.site.register(EcoDriveSites)
admin.site.register(User)


class CarModelsAdmin(admin.ModelAdmin):
    list_display = ['car_model_name', 'average_fuel_efficiency']
    search_fields = ['car_model_name']


# Register your models here.
try:
    admin.site.unregister(CarModels)
except admin.sites.NotRegistered:
    pass

admin.site.register(CarModels, CarModelsAdmin)