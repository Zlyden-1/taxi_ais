from django.contrib import admin

from . import models

admin.site.register(models.Driver)
admin.site.register(models.Vehicle)
admin.site.register(models.VehicleType)
admin.site.register(models.VehicleHistory)
admin.site.register(models.Client)
admin.site.register(models.VehicleLocation)
admin.site.register(models.VehicleStatus)
