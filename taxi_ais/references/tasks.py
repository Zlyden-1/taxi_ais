from django.utils import timezone
from celery import shared_task
from .models import Rent, Contractor


@shared_task
def add_rent_task():
    contractors = Contractor.objects.all()
    for contractor in contractors:
        summ = -contractor.vehicle.vehicle_type.rent_price
        try:
            previous_rent = Rent.objects.order_by('-payment_date', '-time').first()
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
