from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.utils import timezone

from datetime import datetime, timedelta

from .forms import (CreateDriverForm, UpdateDriverForm, CreateVehicleForm, UpdateVehicleForm, CreateRentPaymentForm,
    DateRangeForm)
from .models import (Contractor, Driver, Vehicle, DriverPassportPhoto, DriverPhoto, DrivingLicensePhoto,
    RentingContractPhoto, Rent)


def index(request):
    return render(request, 'references/index.html')


def contractors(request):
    contractors_list = Contractor.objects.all().order_by('-renting_date')
    context = {'contractors': contractors_list,
               'drivers': Driver.objects.filter(status=True),
               'vehicles': Vehicle.objects.filter(status=True),
               }
    return render(request, 'references/contractors.html', context)


def add_contractor(request):
    try:
        new_contractor = Contractor(driver=Driver.objects.get(pk=request.POST['driver']),
                                    vehicle=Vehicle.objects.get(pk=request.POST['vehicle']),
                                    renting_date=request.POST['renting_date'])
    except KeyError:
        return render(request, 'references/error.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        new_contractor.save()
        return HttpResponseRedirect(redirect_to='/references/contractors')


def contractor_detail(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    drivers = Driver.objects.all()
    vehicles = Vehicle.objects.all()
    try:
        balance = contractor.rent_set.latest('payment_date').balance
    except Rent.DoesNotExist:
        balance = 'Нет данных'
    context = {'contractor': contractor,
               'drivers': drivers,
               'vehicles': vehicles,
               'balance': balance,
               'rents': contractor.rent_set.order_by('-payment_date')[:10]}
    return render(request, 'references/contractor.html', context)


def add_contractor_rent(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    payment_date = timezone.localdate()
    time = timezone.localtime()
    try:
        summ = int(request.POST['summ'])
    except KeyError:
        return render(request, 'references/error.html', {
            'error_message': "Вы не ввели сумму",
        })
    else:
        try:
            previous_rent = Rent.objects.order_by('-payment_date', '-time').first()
            if previous_rent is None:
                balance = summ
            else:
                balance = previous_rent.balance + summ
        except Rent.DoesNotExist:
            balance = summ
        rent = Rent(contractor=contractor, payment_date=payment_date, time=time, summ=summ, balance=balance)
        rent.save()
        return HttpResponseRedirect(redirect_to=f'/references/contractor/{contractor.pk}')


def edit_contractor(request, pk):
    try:
        contractor = get_object_or_404(Contractor, pk=pk)
        contractor.driver = Driver.objects.get(pk=request.POST['driver'])
        contractor.vehicle = Vehicle.objects.get(pk=request.POST['vehicle'])
        contractor.renting_date = request.POST['renting_date']
    except KeyError:
        return render(request, 'references/error.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        contractor.save()
        return HttpResponseRedirect(redirect_to='/references/contractors')


def delete_contractor(request, pk):
    contractor = Contractor.objects.get(pk=pk)
    contractor.delete()
    return HttpResponseRedirect(redirect_to='/references/contractors')


def drivers(request):
    if request.method == 'GET':
        form = CreateDriverForm()
        drivers = Driver.objects.all()
        return render(request, 'references/drivers.html', {'form': form, 'drivers': drivers})
    elif request.method == 'POST':
        form = CreateDriverForm(request.POST, request.FILES)
        if form.is_valid():
            driver = Driver.objects.create(first_name=form.cleaned_data['first_name'],
                                           second_name=form.cleaned_data['second_name'],
                                           patronimic=form.cleaned_data['patronimic'],
                                           name=form.cleaned_data['name'],
                                           citizenship=form.cleaned_data['citizenship'],
                                           passport_id=form.cleaned_data['passport_id'],
                                           passport_issue_date=form.cleaned_data['passport_issue_date'],
                                           date_of_birth=form.cleaned_data['date_of_birth'],
                                           place_of_birth=form.cleaned_data['place_of_birth'],
                                           residence_place=form.cleaned_data['residence_place'],
                                           phone_number=form.cleaned_data['phone_number'],
                                           driving_license_id=form.cleaned_data['driving_license_id'],
                                           driving_license_category=form.cleaned_data['driving_license_category'],
                                           driving_license_validity_period=form.cleaned_data[
                                               'driving_license_validity_period'],
                                           rent_sum=form.cleaned_data['rent_sum'],
                                           deposit=form.cleaned_data['deposit'],
                                           comment=form.cleaned_data['comment'],
                                           status=True, )
            save_photos(driver, request, DriverPassportPhoto, 'passport_photo')
            save_photos(driver, request, DriverPhoto, 'photo')
            save_photos(driver, request, DrivingLicensePhoto, 'license_photo')
            save_photos(driver, request, RentingContractPhoto, 'contract_photo')
            return HttpResponseRedirect(redirect_to='/references/drivers')
        else:
            drivers = Driver.objects.all()
            return render(request, 'references/drivers.html', {'form': form, 'drivers': drivers})


def active_drivers(request):
    if request.method == 'GET':
        form = CreateDriverForm()
        drivers = Driver.objects.filter(status=True)
        return render(request, 'references/active_drivers.html', {'form': form, 'drivers': drivers})
    elif request.method == 'POST':
        form = CreateDriverForm(request.POST, request.FILES)
        if form.is_valid():
            driver = Driver.objects.create(first_name=form.cleaned_data['first_name'],
                                           second_name=form.cleaned_data['second_name'],
                                           patronimic=form.cleaned_data['patronimic'],
                                           name=form.cleaned_data['name'],
                                           citizenship=form.cleaned_data['citizenship'],
                                           passport_id=form.cleaned_data['passport_id'],
                                           passport_issue_date=form.cleaned_data['passport_issue_date'],
                                           date_of_birth=form.cleaned_data['date_of_birth'],
                                           place_of_birth=form.cleaned_data['place_of_birth'],
                                           residence_place=form.cleaned_data['residence_place'],
                                           phone_number=form.cleaned_data['phone_number'],
                                           driving_license_id=form.cleaned_data['driving_license_id'],
                                           driving_license_category=form.cleaned_data['driving_license_category'],
                                           driving_license_validity_period=form.cleaned_data[
                                               'driving_license_validity_period'],
                                           rent_sum=form.cleaned_data['rent_sum'],
                                           deposit=form.cleaned_data['deposit'],
                                           comment=form.cleaned_data['comment'],
                                           status=True, )
            save_photos(driver, request, DriverPassportPhoto, 'passport_photo')
            save_photos(driver, request, DriverPhoto, 'photo')
            save_photos(driver, request, DrivingLicensePhoto, 'license_photo')
            save_photos(driver, request, RentingContractPhoto, 'contract_photo')
            return HttpResponseRedirect(redirect_to='/references/drivers')
        else:
            drivers = Driver.objects.filter(status=True)
            return render(request, 'references/active_drivers.html', {'form': form, 'drivers': drivers})


def save_photos(driver, request, photo_instance, key):
    for f in request.FILES.getlist(key):
        data = f.read()
        photo = photo_instance(driver=driver)
        objects = photo_instance.objects.filter(driver=driver)
        if objects:
            number = max([int(object_.filename().split('_')[-1].split('.')[0]) for object_ in objects]) + 1
        else:
            number = 1
        postfix = f.name.split('.')[-1]
        name = f'{driver.name}_passport_photo_{number}.{postfix}'
        photo.photo.save(name, ContentFile(data))
        photo.save()


class DriverDetail(UpdateView):
    model = Driver
    form_class = UpdateDriverForm
    template_name = 'references/driver.html'

    def get_success_url(self):
        return reverse_lazy('contractors:driver', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = DriverPhoto.objects.filter(driver=self.object.pk)
        context['passport'] = DriverPassportPhoto.objects.filter(driver=self.object.pk)
        context['license'] = DrivingLicensePhoto.objects.filter(driver=self.object.pk)
        context['contract'] = RentingContractPhoto.objects.filter(driver=self.object.pk)
        return context


class DriverDeleteView(DeleteView):
    model = Driver
    success_url = reverse_lazy('contractors:drivers')


class DriverPhotoDeleteView(DeleteView):
    model = DriverPhoto
    template_name = 'references/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse('contractors:driver', kwargs={'pk': self.object.driver.pk})


class DrivingLicenceDeleteView(DeleteView):
    model = DrivingLicensePhoto
    template_name = 'references/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse('contractors:driver', kwargs={'pk': self.object.driver.pk})


class DriverPassportPhotoDeleteView(DeleteView):
    model = DriverPassportPhoto
    template_name = 'references/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse('contractors:driver', kwargs={'pk': self.object.driver.pk})


class RentingContractPhotoDeleteView(DeleteView):
    model = RentingContractPhoto
    template_name = 'references/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse('contractors:driver', kwargs={'pk': self.object.driver.pk})


def add_driver_photo(request, pk):
    driver = Driver.objects.get(pk=pk)
    save_photos(driver, request, DriverPhoto, 'photo')
    return HttpResponseRedirect(reverse('contractors:driver', kwargs={'pk': pk}))


def add_driver_passport_photo(request, pk):
    driver = Driver.objects.get(pk=pk)
    save_photos(driver, request, DriverPassportPhoto, 'passport_photo')
    return HttpResponseRedirect(reverse('contractors:driver', kwargs={'pk': pk}))


def add_driving_license_photo(request, pk):
    driver = Driver.objects.get(pk=pk)
    save_photos(driver, request, DrivingLicensePhoto, 'license_photo')
    return HttpResponseRedirect(reverse('contractors:driver', kwargs={'pk': pk}))


def add_renting_contract_photo(request, pk):
    driver = Driver.objects.get(pk=pk)
    save_photos(driver, request, RentingContractPhoto, 'contract_photo')
    return HttpResponseRedirect(reverse('contractors:driver', kwargs={'pk': pk}))


class Vehicles(CreateView):
    model = Vehicle
    form_class = CreateVehicleForm
    template_name = 'references/vehicles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all()
        return context

    def form_valid(self, form):
        vehicle = Vehicle.objects.create(VIN=form.cleaned_data['VIN'],
                                         license_plate=form.cleaned_data['license_plate'],
                                         registration_certificate_id=form.cleaned_data['registration_certificate_id'],
                                         vehicle_passport_id=form.cleaned_data['vehicle_passport_id'],
                                         engine_id=form.cleaned_data['engine_id'],
                                         color=form.cleaned_data['color'],
                                         leasing_contract_id=form.cleaned_data['leasing_contract_id'],
                                         insurance_policy_series=form.cleaned_data['insurance_policy_series'],
                                         insurance_policy_id=form.cleaned_data['insurance_policy_id'],
                                         leasing_contract_date=form.cleaned_data['leasing_contract_date'],
                                         lessor=form.cleaned_data['lessor'],
                                         vehicle_type=form.cleaned_data['vehicle_type'],
                                         manufacture_year=form.cleaned_data['manufacture_year'],
                                         registration_certificate_scan=form.cleaned_data[
                                             'registration_certificate_scan'],
                                         vehicle_passport_scan=form.cleaned_data['vehicle_passport_scan'],
                                         status=form.cleaned_data['status'],
                                         location=form.cleaned_data['location'])
        vehicle.save()
        return HttpResponseRedirect(redirect_to='/references/vehicles')


class ActiveVehicles(CreateView):
    model = Vehicle
    form_class = CreateVehicleForm
    template_name = 'references/active_vehicles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.filter(status=True)
        return context

    def form_valid(self, form):
        vehicle = Vehicle.objects.create(VIN=form.cleaned_data['VIN'],
                                         license_plate=form.cleaned_data['license_plate'],
                                         registration_certificate_id=form.cleaned_data['registration_certificate_id'],
                                         vehicle_passport_id=form.cleaned_data['vehicle_passport_id'],
                                         engine_id=form.cleaned_data['engine_id'],
                                         color=form.cleaned_data['color'],
                                         leasing_contract_id=form.cleaned_data['leasing_contract_id'],
                                         insurance_policy_series=form.cleaned_data['insurance_policy_series'],
                                         insurance_policy_id=form.cleaned_data['insurance_policy_id'],
                                         leasing_contract_date=form.cleaned_data['leasing_contract_date'],
                                         lessor=form.cleaned_data['lessor'],
                                         vehicle_type=form.cleaned_data['vehicle_type'],
                                         manufacture_year=form.cleaned_data['manufacture_year'],
                                         registration_certificate_scan=form.cleaned_data[
                                             'registration_certificate_scan'],
                                         vehicle_passport_scan=form.cleaned_data['vehicle_passport_scan'],
                                         status=True)
        vehicle.save()
        return HttpResponseRedirect(redirect_to='/references/vehicles/active')


class VehicleDetail(UpdateView):
    model = Vehicle
    form_class = UpdateVehicleForm
    template_name = 'references/vehicle.html'

    def get_success_url(self):
        return reverse_lazy('contractors:vehicle', kwargs={'pk': self.object.pk})


class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('contractors:vehicles')


class RentList(CreateView):
    model = Rent
    form_class = CreateRentPaymentForm
    template_name = 'references/rent_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rent_list'] = Rent.objects.order_by('-payment_date', '-time')
        return context

    def form_valid(self, form):
        try:
            previous_rent = Rent.objects.order_by('-payment_date', '-time').first()
            rent = form.save(commit=False)
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
    template_name = 'references/rent_report.html'

    def get(self, request, *args, **kwargs):
        # Определяем даты начала и конца периода по умолчанию
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
        contractors_ = list({rent.contractor for rent in rents})
        contractors_.sort(key=lambda contractor: contractor.driver.name)
        contractors_rents = {}
        daily_total = [0] * len(context['dates'])
        for contractor in contractors_:
            contractors_rents[contractor] = []
            contractor_rents = rents.filter(contractor=contractor).exclude(comment='Автоматическое начисление аренды')
            day_index = 0
            for date in context['dates']:
                current_payments = contractor_rents.filter(payment_date=date)
                if current_payments:
                    sum_ = sum([rent.summ for rent in current_payments])
                else:
                    sum_ = 0
                contractors_rents[contractor].append(sum_)
                daily_total[day_index] += sum_
                day_index += 1
            contractors_rents[contractor].append(sum(contractors_rents[contractor]))
            contractors_rents[contractor].append(rents.filter(contractor=contractor).last().balance)
        daily_total.append(sum(daily_total))
        daily_total.append('')
        contractors_rents['Итого'] = daily_total
        context['rents'] = contractors_rents
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        rent_form = CreateRentPaymentForm(request.POST)
        if rent_form.is_valid():
            try:
                previous_rent = Rent.objects.order_by('-payment_date', '-time').first()
                rent = rent_form.save(commit=False)
                if previous_rent is None:
                    balance = rent.summ
                else:
                    balance = previous_rent.balance + rent.summ
            except Rent.DoesNotExist:
                rent = rent_form.save(commit=False)
                balance = rent.summ
            rent.balance = balance
            rent.time = timezone.localtime()
            print(timezone.localtime())
            rent.save()
            return HttpResponseRedirect(reverse('contractors:rent_report_view'))

        date_range_form = DateRangeForm(request.POST)
        if date_range_form.is_valid():
            start_date = date_range_form.cleaned_data['start_date']
            end_date = date_range_form.cleaned_data['end_date']
            return HttpResponseRedirect(
                reverse('contractors:rent_report_view') + f'?start_date={start_date}&end_date={end_date}')

        context = {'rent_form': rent_form, 'date_range_form': date_range_form}
        return render(request, self.template_name, context)

