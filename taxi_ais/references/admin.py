from django.contrib import admin

from . import models

admin.site.register(models.Rent)
admin.site.register(models.Order)
admin.site.register(models.Driver)
admin.site.register(models.Vehicle)
admin.site.register(models.CarAccident)
admin.site.register(models.VehicleType)
admin.site.register(models.Contractor)
admin.site.register(models.Client)
admin.site.register(models.Expense)
admin.site.register(models.VehicleLocation)
admin.site.register(models.VehicleStatus)
