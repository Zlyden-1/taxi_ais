# Generated by Django 4.1.7 on 2023-05-15 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0026_vehiclelocation_vehiclestatus_vehicle_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='rent_type',
            field=models.CharField(choices=[('А', 'Аренда'), ('В', 'Выкуп')], max_length=1, null=True, verbose_name='Способ использования'),
        ),
    ]
