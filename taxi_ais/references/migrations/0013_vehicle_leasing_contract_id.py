# Generated by Django 4.1.7 on 2023-03-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0012_vehicle_manufacture_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='leasing_contract_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='№ ДЛ'),
        ),
    ]