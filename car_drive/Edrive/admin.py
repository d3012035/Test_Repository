from django.contrib import admin
from .models import Manufacturer, CarModel,MyCar, FuelRecord, EcoDriveSite
from .models import User

admin.site.register(Manufacturer)
admin.site.register(CarModel)
admin.site.register(MyCar)
admin.site.register(FuelRecord)
admin.site.register(EcoDriveSite)
admin.site.register(User)


class CarModelsAdmin(admin.ModelAdmin):
    list_display = ['car_model_name', 'average_fuel_efficiency']
    search_fields = ['car_model_name']


# Register your models here.
try:
    admin.site.unregister(CarModel)
except admin.sites.NotRegistered:
    pass

admin.site.register(CarModel, CarModelsAdmin)