from django.contrib import admin

from .models import Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ["driver", "payment_date", "time", "summ", "balance", "comment"]
    list_filter = ["driver", "comment"]
    search_fields = ["driver", "comment"]
    date_hierarchy = "payment_date"
    ordering = ["driver", "payment_date"]
