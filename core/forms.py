from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'equipment',  # Выбор техники из списка
            'task_description',
            'order_date',
            'order_time',
            'hours',
            'address',
            'customer_name',
            'customer_phone'
        ]
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'order_time': forms.TimeInput(attrs={'type': 'time'}),
            'task_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишите техническое задание...'}),
        }
