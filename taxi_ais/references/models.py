import os

from django.db import models
from django.conf import settings


class Order(models.Model):
    ID = models.IntegerField(primary_key=True, null=False, blank=False)
    client = models.ForeignKey(to='Client', on_delete=models.PROTECT,
                               null=False, blank=False, verbose_name='ИНН заказчика')
    contractor = models.ForeignKey(to='Contractor', on_delete=models.PROTECT,
                                   null=False, blank=False, verbose_name='Исполнитель')
    order_time = models.DateTimeField(null=False, blank=False, verbose_name='Время заказа')
    execution_time = models.DateTimeField(null=False, blank=False, db_index=True, verbose_name='Время исполнения')
    summ = models.IntegerField(null=False, blank=False, verbose_name='Сумма')
    milage = models.FloatField(null=False, blank=False, verbose_name='Километраж')

    def __str__(self):
        return self.ID

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering = ['execution_time']


class Client(models.Model):
    taxpayer_id = models.CharField(primary_key=True, max_length=20, null=False, blank=False, verbose_name='ИНН')
    registration_cause_code = models.CharField(max_length=20, null=False, blank=False, verbose_name='КПП')
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


class Contractor(models.Model):
    driver = models.ForeignKey(to='Driver', on_delete=models.PROTECT,
                               null=False, blank=False, verbose_name='ID водителя')
    vehicle = models.ForeignKey(to='Vehicle', on_delete=models.PROTECT,
                                null=False, blank=False, verbose_name='ID машины')
    renting_date = models.DateField(null=False, blank=False, db_index=True, verbose_name='Дата аренды')

    def __str__(self):
        return f'{self.driver} {self.vehicle}'

    class Meta:
        verbose_name_plural = 'Исполнители'
        verbose_name = 'Исполнитель'


class Driver(models.Model):
    second_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    patronimic = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='ФИО')
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
    rent_sum = models.IntegerField(null=True, blank=True, verbose_name='Аренда')
    deposit = models.IntegerField(null=True, blank=True, verbose_name='Залог')
    status = models.BooleanField(null=False, blank=True, default=True, verbose_name='Статус')

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


class DriverPhoto(models.Model):
    photo = models.ImageField(upload_to='drivers/photos/', verbose_name='Фото водителя')
    driver = models.ForeignKey(to='Driver', on_delete=models.CASCADE, verbose_name='Водитель')

    def filename(self):
        return os.path.basename(self.photo.name)

    def delete(self, *args, **kwargs):
        print(self.photo.path)
        photo_path = self.photo.path
        os.remove(photo_path)
        super().delete(*args, **kwargs)


class DrivingLicensePhoto(models.Model):
    photo = models.ImageField(upload_to='drivers/driving_license_photos/', verbose_name='Фото прав')
    driver = models.ForeignKey(to='Driver', on_delete=models.CASCADE, verbose_name='Водитель')

    def filename(self):
        return os.path.basename(self.photo.name)

    def delete(self, *args, **kwargs):
        photo_path = self.photo.path
        os.remove(photo_path)
        super().delete(*args, **kwargs)


class DriverPassportPhoto(models.Model):
    photo = models.ImageField(upload_to='drivers/passports/', verbose_name='Фото паспорта')
    driver = models.ForeignKey(to='Driver', on_delete=models.CASCADE, verbose_name='Водитель')

    def filename(self):
        return os.path.basename(self.photo.name)

    def delete(self, *args, **kwargs):
        photo_path = self.photo.path
        os.remove(photo_path)
        super().delete(*args, **kwargs)


class RentingContractPhoto(models.Model):
    photo = models.ImageField(upload_to='drivers/renting_contracts/', verbose_name='Фото договора аренды')
    driver = models.ForeignKey(to='Driver', on_delete=models.CASCADE, verbose_name='Водитель')

    def filename(self):
        return os.path.basename(self.photo.name)

    def delete(self, *args, **kwargs):
        photo_path = self.photo.path
        os.remove(photo_path)
        super().delete(*args, **kwargs)


class Vehicle(models.Model):
    VIN = models.CharField(max_length=50, primary_key=True, null=False, blank=False)
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
    status = models.BooleanField(null=False, blank=True, default=True, verbose_name='Статус')

    def rc_filename(self):
        return os.path.basename(self.registration_certificate_scan.name)

    def vp_filename(self):
        return os.path.basename(self.vehicle_passport_scan.name)

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
                                   f'vehicles\\registration_certificates\\{self.registration_certificate_scan.name}')
            os.remove(rc_path)
        if self.vehicle_passport_scan:
            vp_path = os.path.join(settings.MEDIA_ROOT,
                                   f'vehicles\\vehicle_passports\\{self.vehicle_passport_scan.name}')
            os.remove(vp_path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.vehicle_type.model} {self.VIN}'

    class Meta:
        verbose_name_plural = 'Автомобили'
        verbose_name = 'Автомобиль'


class RegistrationCertificateScan(models.Model):
    photo = models.ImageField(upload_to='vehicles/Сканы_СТС', verbose_name='Скан СТС')
    vehicle = models.ForeignKey(to='Vehicle', on_delete=models.CASCADE, verbose_name='ТС')

    def save(self, *args, **kwargs):
        if self.pk is None:
            this_vehicle_photos = RegistrationCertificateScan.objects.filter(vehicle=self.vehicle)
            self.photo.name = f'{self.vehicle}_скан_СТС_{len(this_vehicle_photos) + 1}.jpg'
        else:
            existing_photo = RegistrationCertificateScan.objects.get(pk=self.pk)
            photo_path = existing_photo.photo.path
            postfix = photo_path.split('_')[-1]
            os.remove(photo_path)
            self.photo.name = f'{self.vehicle}_скан_СТС_{postfix}'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        photo_path = self.photo.path
        os.remove(photo_path)
        super().delete(*args, **kwargs)


class VehiclePassportScan(models.Model):
    photo = models.ImageField(upload_to='vehicles/Сканы_ПТС', verbose_name='Скан ПТС')
    vehicle = models.ForeignKey(to='Vehicle', on_delete=models.CASCADE, verbose_name='ТС')

    def save(self, *args, **kwargs):
        if self.pk is None:
            this_vehicle_photos = VehiclePassportScan.objects.filter(vehicle=self.vehicle)
            self.photo.name = f'{self.vehicle}_скан_ПТС_{len(this_vehicle_photos) + 1}.jpg'
        else:
            existing_photo = VehiclePassportScan.objects.get(pk=self.pk)
            photo_path = existing_photo.photo.path
            postfix = photo_path.split('_')[-1]
            os.remove(photo_path)
            self.photo.name = f'{self.vehicle}_скан_ПТС_{postfix}'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        photo_path = self.photo.path
        os.remove(photo_path)
        super().delete(*args, **kwargs)


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


class Rent(models.Model):
    contractor = models.ForeignKey(to='Contractor', on_delete=models.PROTECT,
                                   null=True, blank=False, verbose_name='Исполнитель')
    payment_date = models.DateField(null=False, blank=False, verbose_name='Дата')
    summ = models.FloatField(null=False, blank=False, verbose_name='Сумма')
    balance = models.FloatField(null=True, blank=False, verbose_name='Баланс')
    status = models.ForeignKey(to='RentStatus', on_delete=models.PROTECT,
                               null=False, blank=False, verbose_name='Статус')

    def __str__(self):
        return f'{self.contractor} {self.payment_date}'

    class Meta:
        verbose_name_plural = 'Аренда'
        verbose_name = 'Аренда'


class CarAccident(models.Model):
    date = models.DateField(null=False, blank=False, verbose_name='Дата ДТП')
    contractor = models.ForeignKey(to='Contractor', on_delete=models.PROTECT,
                                   null=True, blank=False, verbose_name='Исполнитель')
    status = models.ForeignKey(to='AccidentStatus', on_delete=models.PROTECT,
                               null=False, blank=False, verbose_name='Статус')
    photo = models.CharField(max_length=200, null=False, blank=False, verbose_name='Фото')

    def __str__(self):
        return f'{self.contractor} {self.date}'

    class Meta:
        verbose_name_plural = 'ДТП'
        verbose_name = 'ДТП'


class Expense(models.Model):
    date = models.DateField(null=False, blank=False, verbose_name='Дата')
    vehicle = models.ForeignKey(to='Vehicle', on_delete=models.PROTECT,
                                null=False, blank=False, verbose_name='ID машины')
    status = models.ForeignKey(to='ExpenseStatus', on_delete=models.PROTECT,
                               null=False, blank=False, verbose_name='Статус')
    summ = models.FloatField(null=False, blank=False, verbose_name='Сумма')

    def __str__(self):
        return f'{self.vehicle} {self.date}'

    class Meta:
        verbose_name_plural = 'Затраты'
        verbose_name = 'Затрата'


class RentStatus(models.Model):
    status = models.CharField(max_length=40, primary_key=True, null=False, blank=False, verbose_name='Статус')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'Статусы аренды'
        verbose_name = 'Статус аренды'


class AccidentStatus(models.Model):
    status = models.CharField(max_length=40, primary_key=True, null=False, blank=False, verbose_name='Статус')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'Статусы ДТП'
        verbose_name = 'Статус ДТП'


class ExpenseStatus(models.Model):
    status = models.CharField(max_length=40, primary_key=True, null=False, blank=False, verbose_name='Статус')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'Статусы затрат'
        verbose_name = 'Статус затраты'
