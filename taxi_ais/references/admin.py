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
admin.site.register(models.AccidentStatus)
admin.site.register(models.ExpenseStatus)
admin.site.register(models.RentStatus)
admin.site.register(models.DriverPassportPhoto)
admin.site.register(models.DriverPhoto)
admin.site.register(models.DrivingLicensePhoto)
admin.site.register(models.RentingContractPhoto)
# Register your models here.
