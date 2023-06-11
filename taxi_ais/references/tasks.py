from datetime import date, time, timedelta

from django.utils import timezone
from celery import shared_task

from .models import Rent, Contractor


@shared_task
def add_rent_task():
    contractors = Contractor.objects.all()
    for contractor in contractors:
        summ = -contractor.vehicle.vehicle_type.rent_price
        try:
            previous_rent = Rent.objects.filter(contractor=contractor).order_by('-payment_date', '-time').first()
            if previous_rent is None:
                balance = summ
            else:
                balance = previous_rent.balance + summ
        except Rent.DoesNotExist:
            balance = summ
        rent = Rent.objects.create(
            contractor=contractor,
            payment_date=timezone.localdate(),
            time=timezone.localtime(),
            summ=summ,
            comment='Автоматическое начисление аренды'
        )
        rent.balance = balance
        rent.save()


# single-use script for restoring the database
@shared_task
def add_current_week_rents():
    contractors = Contractor.objects.all()
    today = date.today()
    start = today - timedelta(days=today.isoweekday())
    dates = [start + timedelta(days=d) for d in range(2, today.isoweekday()+1)]
    for date_ in dates:
        for contractor in contractors:
            summ = -contractor.vehicle.vehicle_type.rent_price
            try:
                previous_rent = Rent.objects.filter(contractor=contractor).order_by('-payment_date', '-time').first()
                if previous_rent is None:
                    balance = summ
                else:
                    balance = previous_rent.balance + summ
            except Rent.DoesNotExist:
                balance = summ
            rent = Rent.objects.create(
                contractor=contractor,
                payment_date=date_,
                time=time(0,0,0),
                summ=summ,
                comment=f'Автоматическое начисление аренды'
            )
            rent.balance = balance
            rent.save()

