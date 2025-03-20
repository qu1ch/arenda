
from django import forms
from .models import Equipment
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['type', 'model', 'price_per_hour', 'load_capacity', 'elevator_height', 'tonnage']
        widgets = {
            'price_per_hour': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Скрываем дополнительные поля, пока не выбран тип
        self.fields['load_capacity'].widget.attrs['style'] = 'display: none'
        self.fields['elevator_height'].widget.attrs['style'] = 'display: none'
        self.fields['tonnage'].widget.attrs['style'] = 'display: none'

    def set_additional_fields(self, equipment_type):
        if equipment_type == 'dump-truck' or equipment_type == 'crane' or equipment_type == 'manipulator-crane':
            self.fields['load_capacity'].widget.attrs['style'] = 'display: block'
        elif equipment_type == 'elevator-crane':
            self.fields['elevator_height'].widget.attrs['style'] = 'display: block'
        elif equipment_type == 'crawler-bulldozer':
            self.fields['tonnage'].widget.attrs['style'] = 'display: block'