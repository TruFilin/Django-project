# Generated by Django 5.1.6 on 2025-02-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forklifts', '0004_alter_forklift_supply_contract_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forklift',
            name='serial_number',
            field=models.CharField(max_length=100),
        ),
    ]
