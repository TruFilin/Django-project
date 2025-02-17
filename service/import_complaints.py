import os
import pandas as pd
import django

# Установите путь к вашему проекту Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')  # Замените на имя вашего проекта
django.setup()

from forklifts.models import Complaint, Forklift  # Замените на ваши модели

# Замените 'data.xlsx' на путь к вашему файлу
data = pd.read_excel('data.xlsx', sheet_name='рекламация output', header=1)  # Укажите имя листа

# Удаляем символы переноса строки и добавляем пробелы
data.columns = data.columns.str.replace('\n', '', regex=True).str.strip()

# Вывод названий столбцов для проверки
print(data.columns.tolist())

# Импорт данных в модель Complaint
complaints = []
for index, row in data.iterrows():
    # Извлечение или создание объекта Forklift для связи
    serial_number = row['Зав. № машины']
    forklift_instance = Forklift.objects.get(serial_number=serial_number)  # Убедитесь, что запись существует

    complaint = Complaint(
        forklift=forklift_instance,
        failure_date=row['Дата отказа'],
        operating_hours=row['Наработка, м/час'],
        failure_node=row['Узел отказа'],
        failure_description=row['Описание отказа'],
        recovery_method=row['Способ восстановления'],
        used_parts=row['Используемые запасные части'],
        recovery_date=row['Дата восстановления'],
        downtime=row['Время простоя техники']
    )
    complaints.append(complaint)

# Сохранение данных в базе данных
Complaint.objects.bulk_create(complaints)

print(f"{len(complaints)} complaint records have been imported.")
