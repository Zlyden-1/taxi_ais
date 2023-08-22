from datetime import date, time, timedelta

from django.utils import timezone
from celery import shared_task

from references.models import Driver
from .models import Rent


@shared_task
def add_rent_task():
    drivers = Driver.objects.exclude(vehicle=None).filter(status=True)
    for driver in drivers:
        summ = -driver.vehicle.vehicle_type.rent_price
        try:
            previous_rent = Rent.objects.filter(driver=driver).order_by("-payment_date", "-time").first()
            if previous_rent is None:
                balance = summ
            else:
                balance = previous_rent.balance + summ
        except Rent.DoesNotExist:
            balance = summ
        rent = Rent.objects.create(
            driver=driver,
            payment_date=timezone.localdate(),
            time=timezone.localtime(),
            summ=summ,
            comment="Автоматическое начисление аренды",
        )
        rent.balance = balance
        rent.save()


# single-use script for restoring the database
@shared_task
def add_current_week_rents():
    drivers = Driver.objects.all()
    today = date.today()
    start = today - timedelta(days=today.isoweekday())
    dates = [start + timedelta(days=d) for d in range(2, today.isoweekday() + 1)]
    for date_ in dates:
        for driver in drivers:
            summ = -driver.vehicle.vehicle_type.rent_price
            try:
                previous_rent = Rent.objects.filter(driver=driver).order_by("-payment_date", "-time").first()
                if previous_rent is None:
                    balance = summ
                else:
                    balance = previous_rent.balance + summ
            except Rent.DoesNotExist:
                balance = summ
            rent = Rent.objects.create(
                driver=driver,
                payment_date=date_,
                time=time(0, 0, 0),
                summ=summ,
                comment=f"Автоматическое начисление аренды",
            )
            rent.balance = balance
            rent.save()
