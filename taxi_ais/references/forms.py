from django import forms
from django.utils import timezone

from .models import Driver, Vehicle


class CreateDriverForm(forms.Form):
    second_name = forms.CharField(max_length=50, required=False, label='Фамилия')
    first_name = forms.CharField(max_length=50, required=False, label='Имя')
    patronimic = forms.CharField(max_length=50, required=False, label='Отчество')
    name = forms.CharField(max_length=50, required=True, label='ФИО')
    citizenship = forms.CharField(max_length=50, required=False, label='Гражданство')
    passport_id = forms.CharField(max_length=200, required=False, label='Номер паспорта')
    passport_issue_date = forms.DateField(required=False, label='Дата выдачи паспорта')
    date_of_birth = forms.DateField(required=False, label='Дата рождения')
    place_of_birth = forms.CharField(max_length=150, required=False, label='Место рождения')
    residence_place = forms.CharField(max_length=150, required=False, label='Место жительства')
    phone_number = forms.CharField(max_length=12, required=False, label='Номер телефона')
    driving_license_id = forms.CharField(max_length=20, required=False, label='Номер прав')
    driving_license_category = forms.CharField(max_length=30, required=False, label='Категория')
    driving_license_validity_period = forms.DateField(required=False, label='Срок действия')
    deposit = forms.IntegerField(required=False, label='Залог')
    photo = forms.ImageField(required=False, label='Фото водителя',
                             widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    passport_photo = forms.ImageField(required=False, label='Фото паспорта',
                                      widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    license_photo = forms.ImageField(required=False, label='Фото прав',
                                     widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    contract_photo = forms.ImageField(required=False, label='Фото договора аренды',
                                      widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    comment = forms.CharField(required=False, label='Комментарий', widget=forms.TextInput())


class UpdateDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('second_name', 'first_name', 'patronimic', 'name', 'citizenship', 'passport_id',
                  'passport_issue_date', 'date_of_birth', 'place_of_birth', 'residence_place', 'phone_number',
                  'driving_license_id', 'driving_license_category', 'driving_license_validity_period',
                  'deposit', 'status', 'comment')


class CreateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('VIN', 'license_plate', 'registration_certificate_id', 'vehicle_passport_id', 'engine_id', 'color',
                  'leasing_contract_id', 'insurance_policy_series', 'insurance_policy_id', 'leasing_contract_date',
                  'lessor', 'vehicle_type', 'manufacture_year', 'registration_certificate_scan',
                  'vehicle_passport_scan', 'status', 'location', 'rent_type')
        widgets = {'registration_certificate_scan': forms.FileInput(attrs={'accept': '.pdf'}),
                   'vehicle_passport_scan': forms.FileInput(attrs={'accept': '.pdf'})}


class UpdateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('VIN', 'license_plate', 'registration_certificate_id', 'vehicle_passport_id', 'engine_id', 'color',
                  'leasing_contract_id', 'insurance_policy_series', 'insurance_policy_id', 'leasing_contract_date',
                  'lessor', 'vehicle_type', 'manufacture_year', 'registration_certificate_scan',
                  'vehicle_passport_scan', 'status', 'location', 'rent_type')

