import os

from django.db import models
from django.conf import settings


class Client(models.Model):
    taxpayer_id = models.CharField(primary_key=True, max_length=20, 
                                   null=False, blank=False, verbose_name='ИНН')
    registration_cause_code = models.CharField(max_length=20, null=False, blank=False, 
                                               verbose_name='КПП')
    main_state_registration_number = models.CharField(max_length=20, null=False, blank=False, verbose_name='ОГРН')
    business_activity_code = models.CharField(max_length=20, null=False, blank=False, verbose_name='ОКВЭД')
    organisation = models.CharField(max_length=150, db_index=True,
                                    null=False, blank=False, verbose_name='Наименование организации')
    address = models.CharField(max_length=150, db_index=True, null=False, blank=False, verbose_name='Адрес')
    payment_account = models.CharField(max_length=20, null=False, blank=False, verbose_name='р/с')
    bank_name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Банк')
    bank_id = models.CharField(max_length=9, null=False, blank=False, verbose_name='БИК')
    correspondent_account = models.CharField(max_length=20, null=False, blank=False, verbose_name='к/с')
    client_post = models.CharField(max_length=20, null=False, blank=False, verbose_name='Должность')
    client_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='ФИО')
    documents = models.TextField(null=True, blank=True, default=None, verbose_name='Сканы документов')

    def __str__(self):
        return self.organisation

    class Meta:
        verbose_name_plural = 'Заказчики'
        verbose_name = 'Заказчик'
        ordering = ['organisation']


class VehicleHistory(models.Model):
    driver = models.ForeignKey(to='Driver', on_delete=models.CASCADE,
                               null=False, blank=False, verbose_name='Водитель')
    vehicle = models.ForeignKey(to='Vehicle', on_delete=models.CASCADE,
                                null=False, blank=False, verbose_name='ТС')
    renting_date = models.DateField(null=False, blank=False, verbose_name='Дата взятия в аренду')
    renting_end_date = models.DateField(null=True, blank=True, verbose_name='Дата сдачи')

    def __str__(self):
        if self.renting_end_date:
            return f'{self.driver} {self.vehicle} с {self.renting_date} по {self.renting_end_date}'
        else:
            return f'{self.driver} {self.vehicle} с {self.renting_date} по сегодня'

    class Meta:
        verbose_name_plural = 'Исполнители'
        verbose_name = 'Исполнитель'


class Driver(models.Model):
    second_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    patronimic = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    name = models.CharField(max_length=50, verbose_name='ФИО')
    citizenship = models.CharField(max_length=50, null=True, blank=True, verbose_name='Гражданство')
    passport_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='Номер паспорта')
    passport_issue_date = models.DateField(null=True, blank=True, verbose_name='Дата выдачи паспорта')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    place_of_birth = models.CharField(max_length=150, null=True, blank=True, verbose_name='Место рождения')
    residence_place = models.CharField(max_length=150, null=True, blank=True, verbose_name='Место жительства')
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name='Номер телефона')
    driving_license_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер прав')
    driving_license_category = models.CharField(max_length=30, null=True, blank=True, verbose_name='Категория')
    driving_license_validity_period = models.DateField(null=True, blank=True, verbose_name='Срок действия')
    deposit = models.IntegerField(null=True, blank=True, verbose_name='Залог')
    status = models.BooleanField(null=False, blank=True, default=True, verbose_name='Статус')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    telegram_id = models.CharField(max_length=33, null=True, blank=True, verbose_name='Тег в телеграм')

    def delete(self, *args, **kwargs):
        for photo in self.driverphoto_set.all():
            photo.delete()
        for photo in self.drivinglicensephoto_set.all():
            photo.delete()
        for photo in self.driverpassportphoto_set.all():
            photo.delete()
        for photo in self.rentingcontractphoto_set.all():
            photo.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        if self.name is None:
            return self.second_name
        return self.name

    class Meta:
        verbose_name_plural = 'Водители'
        verbose_name = 'Водитель'


class AbstractDriverPhoto(models.Model):
    photo = models.ImageField(upload_to=...)
    driver = models.ForeignKey(to='Driver', on_delete=models.CASCADE, verbose_name='Водитель')

    def __str__(self):
        return self.name
    
    def filename(self):
        return os.path.basename(self.photo.name)

    def delete(self, *args, **kwargs):
        photo_path = self.photo.path
        if os.path.exists(photo_path):
            os.remove(photo_path)        
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True


class DriverPhoto(AbstractDriverPhoto):
    photo = models.ImageField(upload_to='drivers/photos/', verbose_name='Фото водителя')


class DrivingLicensePhoto(AbstractDriverPhoto):
    photo = models.ImageField(upload_to='drivers/driving_license_photos/', verbose_name='Фото прав')


class DriverPassportPhoto(AbstractDriverPhoto):
    photo = models.ImageField(upload_to='drivers/passports/', verbose_name='Фото паспорта')


class RentingContractPhoto(AbstractDriverPhoto):
    photo = models.ImageField(upload_to='drivers/renting_contracts/', verbose_name='Фото договора аренды')


class Vehicle(models.Model):
    rent_type_choices = [('А', 'Аренда'), ('В', 'Выкуп')]  # А и В здесь - русские буквы

    VIN = models.CharField(max_length=50, primary_key=True, null=False, blank=False, unique = True)
    license_plate = models.CharField(max_length=10, null=True, blank=True, verbose_name='Гос. номер')
    registration_certificate_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='№ СТС')
    vehicle_passport_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='№ ПТС')
    engine_id = models.CharField(max_length=17, null=True, blank=True, verbose_name='№ двигателя')
    color = models.CharField(max_length=20, null=True, blank=True, verbose_name='Цвет')
    leasing_contract_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='№ ДЛ')
    insurance_policy_series = models.CharField(max_length=3, null=True, blank=True, verbose_name='Серия полиса')
    insurance_policy_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='Номер полиса')
    leasing_contract_date = models.DateField(null=True, blank=True, verbose_name='Дата ДЛ')
    lessor = models.CharField(max_length=50, null=True, blank=True, verbose_name='Лизингодатель')
    vehicle_type = models.ForeignKey(to='VehicleType', on_delete=models.PROTECT,
                                     null=True, blank=True, verbose_name='Тип ТС')
    manufacture_year = models.IntegerField(null=True, blank=True, verbose_name='Год выпуска')
    registration_certificate_scan = models.FileField(upload_to='vehicles/registration_certificates/',
                                                     null=True, blank=True, verbose_name='Скан СТС')
    vehicle_passport_scan = models.FileField(upload_to='vehicles/vehicle_passports/',
                                             null=True, blank=True, verbose_name='Скан ПТС')
    status = models.ForeignKey(to='VehicleStatus', on_delete=models.PROTECT,
                               null=True, blank=False, verbose_name='Статус')
    location = models.ForeignKey(to='VehicleLocation', on_delete=models.PROTECT,
                                 null=True, blank=False, verbose_name='Место базирования')
    rent_type = models.CharField(max_length=1, choices=rent_type_choices, null=True, blank=False,
                                 verbose_name='Способ использования')
    driver = models.OneToOneField(to=Driver, on_delete=models.SET_NULL, related_name='vehicle',
                                  null=True, blank=True, verbose_name="Водитель")
    usage_history = models.ManyToManyField(to=Driver, through=VehicleHistory, related_name='vehicles_history',
                                           verbose_name="История использования")
    acceptance_certificate_scan = models.FileField(upload_to='vehicles/acceptance_certificates/', 
                                                   null=True, blank=True, verbose_name='Акт приема-передачи')
    leasing_contract_scan = models.FileField(upload_to='vehicles/leasing_contracts/', 
                                             null=True, blank=True, verbose_name='Договор лизинга')

    def filename(self, file_field):
        return os.path.basename(self.file_field.name)

    def vp_filename(self):
        return os.path.basename(self.file_field.name)

    def save(self, *args, **kwargs):
        if self.registration_certificate_scan:
            rc_postfix = self.registration_certificate_scan.name.split('.')[-1]
            self.registration_certificate_scan.name = f'{self.VIN}_скан_СТС.{rc_postfix}'
        if self.vehicle_passport_scan:
            vp_postfix = self.vehicle_passport_scan.name.split('.')[-1]
            self.vehicle_passport_scan.name = f'{self.VIN}_скан_ПТС.{vp_postfix}'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.registration_certificate_scan:
            rc_path = os.path.join(settings.MEDIA_ROOT,
                                   f'vehicles/registration_certificates/{self.registration_certificate_scan.name}')
            os.remove(rc_path)
        if self.vehicle_passport_scan:
            vp_path = os.path.join(settings.MEDIA_ROOT,
                                   f'vehicles/vehicle_passports/{self.vehicle_passport_scan.name}')
            os.remove(vp_path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.vehicle_type.model} {self.license_plate}'

    class Meta:
        verbose_name_plural = 'Автомобили'
        verbose_name = 'Автомобиль'


class VehicleLocation(models.Model):
    place = models.CharField(max_length=300, verbose_name='Место')

    def __str__(self):
        return self.place

    class Meta:
        verbose_name_plural = 'Локации автомобилей'
        verbose_name = 'Локация автомобилей'


class VehicleStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус')
    is_active = models.BooleanField(verbose_name='Активно')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Статусы ТС'
        verbose_name = 'Статус ТС'


class VehicleType(models.Model):
    brand = models.CharField(max_length=20, null=False, blank=False, verbose_name='Марка ТС')
    model = models.CharField(max_length=40, null=False, blank=False, verbose_name='Модель ТС')
    power = models.FloatField(null=True, blank=True, verbose_name='Мощность')
    vehicle_type = models.CharField(max_length=40, null=False, blank=False, verbose_name='Тип ТС')
    manufacturer = models.CharField(max_length=100, null=False, blank=False, verbose_name='Производитель')
    has_gas_cylinder_equipment = models.BooleanField(null=False, blank=True, default=False, verbose_name='ГБО')
    rent_price = models.IntegerField(null=True, blank=True, verbose_name='Аренда')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name_plural = 'Типы ТС'
        verbose_name = 'Тип ТС'

