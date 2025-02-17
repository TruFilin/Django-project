from django.db import models
from django.contrib.auth.models import User


class TransmissionModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # Возвращаем имя модели


class ServiceType(models.Model):
    name = models.CharField(max_length=100)

class Organization(models.Model):
    name = models.CharField(max_length=100)

class FailureNode(models.Model):
    name = models.CharField(max_length=100)

class RecoveryMethod(models.Model):
    name = models.CharField(max_length=100)
class BridgeModel(models.Model):
    name = models.CharField(max_length=100)

    class DriveBridgeModel(models.Model):
        name = models.CharField(max_length=100)

    class ControlledBridgeModel(models.Model):
        name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # Возвращаем имя модели
class EngineModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # Возвращаем имя модели


class Forklift(models.Model):
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    engine_model = models.ForeignKey(EngineModel, on_delete=models.CASCADE, related_name='engine_model')
    engine_serial_number = models.CharField(max_length=100)
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.CASCADE)
    transmission_serial_number = models.CharField(max_length=100)
    drive_bridge_model = models.ForeignKey(BridgeModel, related_name='drive_bridge', on_delete=models.CASCADE)
    drive_bridge_serial_number = models.CharField(max_length=100)
    controlled_bridge_model = models.ForeignKey(BridgeModel, related_name='controlled_bridge', on_delete=models.CASCADE)
    controlled_bridge_serial_number = models.CharField(max_length=100)
    supply_contract_number = models.CharField(max_length=100, blank=True, null=True)  # Теперь может быть пустым
    supply_contract_date = models.DateField(blank=True, null=True)  # Теперь может быть пустым
    shipment_date = models.DateField()
    consignee = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=255)
    configuration = models.TextField()
    client = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    service_company = models.ForeignKey(User, related_name='service_companies', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.serial_number} - {self.model}"

class ServiceType(models.Model):
    name = models.CharField(max_length=100)

class Organization(models.Model):
    name = models.CharField(max_length=100)

class TechnicalService(models.Model):
    forklift = models.ForeignKey(Forklift, on_delete=models.CASCADE)  # Связь с моделью Forklift
    service_type = models.CharField(max_length=100)  # Вид ТО
    maintenance_date = models.DateField()  # Дата проведения ТО
    operating_hours = models.FloatField()  # Наработка, м/час
    order_number = models.CharField(max_length=100)  # № заказ-наряда
    order_date = models.DateField()  # Дата заказ-наряда
    organization = models.CharField(max_length=100)  # Организация, проводившая ТО

    def __str__(self):
        return f"{self.forklift.serial_number} - {self.service_type}"
class FailureNode(models.Model):
    name = models.CharField(max_length=100)

class RecoveryMethod(models.Model):
    name = models.CharField(max_length=100)

class Complaint(models.Model):
    forklift = models.ForeignKey(Forklift, on_delete=models.CASCADE)  # Связь с моделью Forklift
    failure_date = models.DateField()  # Дата отказа
    operating_hours = models.FloatField()  # Наработка, м/час
    failure_node = models.CharField(max_length=100)  # Узел отказа
    failure_description = models.TextField()  # Описание отказа
    recovery_method = models.CharField(max_length=100)  # Способ восстановления
    used_parts = models.TextField()  # Используемые запасные части
    recovery_date = models.DateField()  # Дата восстановления
    downtime = models.FloatField()  # Время простоя техники

    def __str__(self):
        return f"{self.forklift.serial_number} - {self.failure_node}"
