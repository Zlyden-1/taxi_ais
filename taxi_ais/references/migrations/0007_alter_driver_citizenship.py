# Generated by Django 4.1.7 on 2023-03-15 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0006_alter_driver_passport_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='citizenship',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Гражданство'),
        ),
    ]
