# Generated by Django 4.1.7 on 2023-03-15 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0002_alter_accidentstatus_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicletype',
            name='power',
            field=models.FloatField(blank=True, null=True, verbose_name='Мощность'),
        ),
    ]
