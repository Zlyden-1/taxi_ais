from django import forms
from .models import Driver, DriverPassportPhoto, DrivingLicensePhoto, DriverPhoto, RentingContractPhoto


class DriverForm(forms.Form):
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
    rent_sum = forms.IntegerField(required=False, label='Аренда')
    deposit = forms.IntegerField(required=False, label='Залог')
    photo = forms.ImageField(required=False, label='Фото водителя',
                             widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    passport_photo = forms.ImageField(required=False, label='Фото паспорта',
                                      widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    license_photo = forms.ImageField(required=False, label='Фото прав',
                                     widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    contract_photo = forms.ImageField(required=False, label='Фото договора аренды',
                                      widget=forms.FileInput(attrs={'multiple': 'multiple'}))


class UpdateDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('second_name', 'first_name', 'patronimic', 'name', 'citizenship', 'passport_id',
                  'passport_issue_date', 'date_of_birth', 'place_of_birth', 'residence_place', 'phone_number',
                  'driving_license_id', 'driving_license_category', 'driving_license_validity_period', 'rent_sum',
                  'deposit', 'status')
        widgets = {'status': forms.Select(choices=((True, 'Активен'), (False, 'Неактивен')))}


class CreateVehicleForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('second_name', 'first_name', 'patronimic', 'name', 'citizenship', 'passport_id',
                  'passport_issue_date', 'date_of_birth', 'place_of_birth', 'residence_place', 'phone_number',
                  'driving_license_id', 'driving_license_category', 'driving_license_validity_period', 'rent_sum',
                  'deposit', 'status')

