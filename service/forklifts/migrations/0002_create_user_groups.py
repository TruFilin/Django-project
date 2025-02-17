# your_app_name/migrations/0002_create_user_groups.py

from django.db import migrations


def create_user_groups(apps, schema_editor):
    from django.contrib.auth.models import Group

    # Создание групп пользователей
    Group.objects.get_or_create(name='Клиент')
    Group.objects.get_or_create(name='Сервисная организация')
    Group.objects.get_or_create(name='Менеджер')


class Migration(migrations.Migration):
    dependencies = [
        ('forklifts', '0001_initial'),  # Замените на вашу последнюю миграцию
    ]

    operations = [
        migrations.RunPython(create_user_groups),
    ]

