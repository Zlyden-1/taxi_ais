# Generated by Django 4.1.7 on 2023-03-14 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=40, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('taxpayer_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ИНН')),
                ('registration_cause_code', models.IntegerField(verbose_name='КПП')),
                ('main_state_registration_number', models.IntegerField(verbose_name='ОГРН')),
                ('business_activity_code', models.CharField(max_length=20, verbose_name='ИНН')),
                ('organisation', models.CharField(db_index=True, max_length=50, verbose_name='Организация')),
                ('address', models.CharField(db_index=True, max_length=150, verbose_name='Адрес')),
                ('payment_account', models.CharField(max_length=20, verbose_name='р/с')),
                ('bank_name', models.CharField(max_length=50, verbose_name='Банк')),
                ('bank_id', models.CharField(max_length=9, verbose_name='БИК')),
                ('correspondent_account', models.CharField(max_length=20, verbose_name='к/с')),
                ('client_post', models.CharField(max_length=20, verbose_name='Должность')),
                ('client_name', models.CharField(max_length=50, verbose_name='ФИО')),
            ],
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('renting_date', models.DateField(verbose_name='Дата аренды')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='ФИО')),
                ('citizenship', models.CharField(max_length=20, verbose_name='Гражданство')),
                ('passport_id', models.CharField(max_length=20, verbose_name='Номер паспорта')),
                ('passport_issue_date', models.DateField(verbose_name='Дата выдачи паспорта')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('place_of_birth', models.CharField(max_length=150, verbose_name='Место рождения')),
                ('residence_place', models.CharField(max_length=150, verbose_name='Место жительства')),
                ('phone_number', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('driving_license_id', models.CharField(max_length=10, verbose_name='Номер прав')),
                ('driving_license_category', models.CharField(max_length=15, verbose_name='Категория')),
                ('driving_license_validity_period', models.DateField(verbose_name='Срок действия')),
                ('rent_sum', models.IntegerField(verbose_name='Аренда')),
                ('deposit', models.IntegerField(verbose_name='Залог')),
                ('photo_link', models.CharField(max_length=200, verbose_name='Фото')),
                ('passport_photo', models.CharField(max_length=200, verbose_name='Фото паспорта')),
                ('driving_license_photo', models.CharField(max_length=200, verbose_name='Фото паспорта')),
                ('rent_photo', models.CharField(max_length=200, verbose_name='Фото паспорта')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=40, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='RentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=40, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20, verbose_name='Марка ТС')),
                ('model', models.CharField(max_length=40, verbose_name='Модель ТС')),
                ('power', models.FloatField(verbose_name='Мощность')),
                ('vehicle_type', models.CharField(max_length=40, verbose_name='Тип ТС')),
                ('manufacturer', models.CharField(max_length=40, verbose_name='Производитель')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('VIN', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('license_plate', models.CharField(max_length=6, verbose_name='Гос. номер')),
                ('registration_certificate_id', models.CharField(max_length=10, verbose_name='№ СТС')),
                ('vehicle_passport_id', models.CharField(max_length=10, verbose_name='№ ПТС')),
                ('engine_id', models.CharField(max_length=17, verbose_name='№ двигателя')),
                ('color', models.CharField(max_length=20, verbose_name='Цвет')),
                ('prefix', models.CharField(max_length=20, verbose_name='Префикс ДЛ')),
                ('postfix', models.CharField(max_length=20, verbose_name='Постфикс ДЛ')),
                ('leasing_contract_date', models.DateField(verbose_name='Дата ДЛ')),
                ('lessor', models.CharField(max_length=50, verbose_name='Лизингодатель')),
                ('registration_certificate_scan', models.CharField(max_length=200, verbose_name='Скан СТС')),
                ('vehicle_passport_scan', models.CharField(max_length=200, verbose_name='Скан ПТС')),
                ('vehicle_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.vehicletype', verbose_name='Тип ТС')),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(verbose_name='Дата')),
                ('summ', models.FloatField(verbose_name='Сумма')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.driver', verbose_name='ID водителя')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.rentstatus', verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('order_time', models.DateTimeField(verbose_name='Время заказа')),
                ('execution_time', models.DateTimeField(db_index=True, verbose_name='Время исполнения')),
                ('summ', models.IntegerField(verbose_name='Сумма')),
                ('milage', models.FloatField(verbose_name='Километраж')),
                ('client_taxpayer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.client', verbose_name='ИНН заказчика')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.contractor', verbose_name='Исполнитель')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('summ', models.FloatField(verbose_name='Сумма')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.expensestatus', verbose_name='Статус')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.vehicle', verbose_name='ID машины')),
            ],
        ),
        migrations.AddField(
            model_name='contractor',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.driver', verbose_name='ID водителя'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.vehicle', verbose_name='ID машины'),
        ),
        migrations.CreateModel(
            name='CarAccident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата ДТП')),
                ('photo', models.CharField(max_length=200, verbose_name='Фото')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.accidentstatus', verbose_name='Статус')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='references.vehicle', verbose_name='ID машины')),
            ],
        ),
    ]
