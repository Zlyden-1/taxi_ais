# Generated by Django 4.1.7 on 2023-05-10 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0022_alter_vehicle_registration_certificate_scan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='status',
        ),
        migrations.DeleteModel(
            name='RentStatus',
        ),
    ]