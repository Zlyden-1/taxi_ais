from django.utils import timezone
from celery import shared_task
from .models import Rent, Contractor


@shared_task
def add_rent_task():
    contractors = Contractor.objects.all()
    for contractor in contractors:
        summ = -contractor.vehicle.vehicle_type.rent_price
        try:
            previous_rent = Rent.objects.order_by('-payment_date').first()
            if previous_rent is None:
                balance = summ
            else:
                balance = previous_rent.balance + summ
        except Rent.DoesNotExist:
            balance = summ
        rent = Rent.objects.create(
            contractor=contractor,
            payment_date=timezone.now().date(),
            summ=-contractor.vehicle.vehicle_type.rent_price,
        )
        rent.balance = balance
        rent.save()
