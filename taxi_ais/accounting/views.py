from datetime import datetime, timedelta

from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.utils import timezone

from references.models import Driver
from .models import Rent
from .forms import CreateRentPaymentForm, DateRangeForm

class RentListView(CreateView):
    model = Rent
    form_class = CreateRentPaymentForm
    template_name = 'accounting/rent_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rent_list'] = Rent.objects.order_by('-payment_date', '-time')
        return context

    def form_valid(self, form):
        try:
            rent = form.save(commit=False)
            previous_rent = Rent.objects.filter(driver_id=rent.driver.id).order_by('-payment_date', '-time').first()
            if previous_rent is None:
                balance = rent.summ
            else:
                balance = previous_rent.balance + rent.summ
        except Rent.DoesNotExist:
            rent = form.save(commit=False)
            balance = rent.summ
        rent.balance = balance
        rent.time = timezone.localtime()
        rent.save()
        return HttpResponseRedirect(redirect_to='/references/rent_list')



class RentReportView(TemplateView):
    template_name = 'accounting/rent_report.html'

    def get(self, request, *args, **kwargs):
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        start_date = request.GET.get('start_date', last_week)
        end_date = request.GET.get('end_date', today)
        rent_form = CreateRentPaymentForm()
        date_range_form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})

        context = {
            'rent_form': rent_form,
            'date_range_form': date_range_form,
        }
        rents = Rent.objects.filter(
            payment_date__range=[start_date, end_date]).order_by('payment_date', 'time')
        context['dates'] = list({rent.payment_date for rent in rents})
        context['dates'].sort()
        drivers_ = list({rent.driver for rent in rents})
        drivers_.sort(key=lambda driver: driver.name)
        drivers_rents = {}
        daily_total = [0] * len(context['dates'])
        for driver in drivers_:
            drivers_rents[driver] = []
            driver_rents = rents.filter(driver=driver).exclude(comment='Автоматическое начисление аренды')
            day_index = 0
            for date in context['dates']:
                current_payments = driver_rents.filter(payment_date=date)
                if current_payments:
                    sum_ = sum([rent.summ for rent in current_payments])
                else:
                    sum_ = 0
                drivers_rents[driver].append(sum_)
                daily_total[day_index] += sum_
                day_index += 1
            drivers_rents[driver].append(sum(drivers_rents[driver]))
            drivers_rents[driver].append(rents.filter(driver=driver).last().balance)
        daily_total.append(sum(daily_total))
        daily_total.append('')
        drivers_rents['Итого'] = daily_total
        context['rents'] = drivers_rents
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        rent_form = CreateRentPaymentForm(request.POST)
        rent = rent_form.save(commit=False)
        date_range_form = DateRangeForm(request.POST)
        if rent_form.is_valid():
            try:
                previous_rent = Rent.objects.filter(driver_id=rent.driver.id).order_by('-payment_date', '-time').first()
                if previous_rent is None:
                    balance = rent.summ
                else:
                    balance = previous_rent.balance + rent.summ
            except Rent.DoesNotExist:
                balance = rent.summ
            rent.balance = balance
            rent.time = timezone.localtime()
            rent.save()
            if date_range_form.is_valid():
                start_date = date_range_form.cleaned_data['start_date']
                end_date = date_range_form.cleaned_data['end_date']
                return HttpResponseRedirect(
                    reverse('references:rent_report') + f'?start_date={start_date}&end_date={end_date}')
            return HttpResponseRedirect(reverse('references:rent_report'))
        context = {'rent_form': rent_form, 'date_range_form': date_range_form}
        return render(request, self.template_name, context)