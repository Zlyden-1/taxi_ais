# Generated by Django 4.1.7 on 2023-03-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0007_alter_driver_citizenship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driving_license_id',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер прав'),
        ),
    ]