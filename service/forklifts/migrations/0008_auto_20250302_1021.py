from django.db import migrations

def update_serial_numbers(apps, schema_editor):
    ModelName = apps.get_model('forklifts', 'Forklift')
    for obj in ModelName.objects.all():
        if obj.serial_number.isdigit():
            obj.serial_number = f"00{obj.serial_number}"
            obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('forklifts', '0007_remove_complaint_service_company_and_more'),  # Укажите предыдущую миграцию
    ]

    operations = [
        migrations.RunPython(update_serial_numbers),
    ]