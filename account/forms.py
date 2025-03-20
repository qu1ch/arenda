
from django import forms

from django import forms
from core.models import RentalRequest


class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ['equipment', 'name', 'lifting_capacity', 'boom_reach', 'lift_height', 'body_volume', 'number',
                  'sts_number', 'driver_license', 'passport_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Поле "driver" не отображается в форме, заполняется автоматически
        self.fields['equipment'].required = True
        self.fields['name'].required = True
        self.fields['number'].required = True

