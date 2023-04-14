from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from .forms import DriverForm, UpdateDriverForm, CreateVehicleForm, UpdateVehicleForm
from .models import Contractor, Driver, Vehicle, DriverPassportPhoto, DriverPhoto, DrivingLicensePhoto, \
    RentingContractPhoto


def index(request):
    return render(request, 'references/index.html')


def contractors(request):
    contractors_list = Contractor.objects.all().order_by('-renting_date')
    context = {'contractors': contractors_list,
               'drivers': Driver.objects.filter(status=True),
               'vehicles': Vehicle.objects.filter(status=True)}
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
    contractor = Contractor.objects.get(pk=pk)
    drivers = Driver.objects.all()
    vehicles = Vehicle.objects.all()
    context = {'contractor': contractor,
               'drivers': drivers,
               'vehicles': vehicles}
    return render(request, 'references/contractor.html', context)


def edit_contractor(request, pk):
    try:
        contractor = Contractor.objects.get(pk=pk)
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
        form = DriverForm()
        drivers = Driver.objects.all()
        return render(request, 'references/drivers.html', {'form': form, 'drivers': drivers})
    elif request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
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
                                           status=True,)
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
        form = DriverForm()
        drivers = Driver.objects.filter(status=True)
        return render(request, 'references/active_drivers.html', {'form': form, 'drivers': drivers})
    elif request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
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
                                           status=True,)
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
                                         status=True)
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

