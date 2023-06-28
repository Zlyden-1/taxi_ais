# Generated by Django 4.1.7 on 2023-03-15 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0014_vehicle_insurance_policy_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='business_activity_code',
            field=models.CharField(max_length=20, verbose_name='ОКВЭД'),
        ),
        migrations.AlterField(
            model_name='client',
            name='main_state_registration_number',
            field=models.CharField(max_length=20, verbose_name='ОГРН'),
        ),
        migrations.AlterField(
            model_name='client',
            name='registration_cause_code',
            field=models.CharField(max_length=20, verbose_name='КПП'),
        ),
        migrations.AlterField(
            model_name='client',
            name='taxpayer_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='ИНН'),
        ),
    ]