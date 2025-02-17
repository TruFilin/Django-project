from django import forms
from .models import Forklift, TechnicalService, Complaint  # Импортируйте ваши модели

class ForkliftForm(forms.ModelForm):
    class Meta:
        model = Forklift
        fields = [
            'serial_number',
            'model',
            'engine_model',
            'engine_serial_number',
            'transmission_model',
            'transmission_serial_number',
            'drive_bridge_model',
            'drive_bridge_serial_number',
            'controlled_bridge_model',
            'controlled_bridge_serial_number',
            'shipment_date',
            'consignee',
            'delivery_address',
            'configuration',
            'client',
            'service_company',
        ]

class TechnicalServiceForm(forms.ModelForm):
    class Meta:
        model = TechnicalService
        fields = [
            'service_type',
            'maintenance_date',
            'operating_hours',
            'order_number',
            'order_date',
            'organization',
            'forklift',  # Если вас интересует, чтобы пользователь выбирал погрузчик
        ]

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'failure_date',
            'operating_hours',
            'failure_node',
            'failure_description',
            'recovery_method',
            'used_parts',
            'recovery_date',
            'downtime',
            'forklift',  # Если вас интересует, чтобы пользователь выбирал погрузчик
        ]
