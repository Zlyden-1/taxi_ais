from django.contrib import admin

from .models import Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ["driver", "payment_date", "time", "summ", "balance", "comment"]
    list_filter = ["driver", "comment"]
    search_fields = ["driver", "comment"]
    date_hierarchy = "payment_date"
    ordering = ["-payment_date", "-time"]
    readonly_fields = ["driver", "payment_date", "time", "balance"]

    # TODO: переопределить форму изменения
    def save_model(self, request, obj, form, change):
        previous_rent = (
            Rent.objects.filter(driver=obj.driver, payment_date=obj.payment_date, time__lt=obj.time)
            .order_by("payment_date", "time")
            .last()
        )
        that_day_rents = Rent.objects.filter(
            driver=obj.driver, payment_date=obj.payment_date, time__gte=obj.time
        ).order_by("payment_date", "time")
        later_rents = Rent.objects.filter(driver=obj.driver, payment_date__gt=obj.payment_date).order_by(
            "payment_date", "time"
        )
        for rents in that_day_rents, later_rents:
            for rent in rents:
                if previous_rent:
                    rent.balance = rent.summ + previous_rent.balance
                else:
                    rent.balance = rent.summ
                previous_rent = rent
                rent.save()
