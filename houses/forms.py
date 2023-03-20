from django import forms
from .models import MeterReading

class MeterReadingForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        fields = ['house', 'current_reading']
        widgets = {
            'house': forms.HiddenInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        house = cleaned_data['house']
        current_reading = cleaned_data['current_reading']
        previous_reading = house.current_meter_reading.previous_reading
        if current_reading <= previous_reading:
            raise forms.ValidationError("Current reading must be greater than previous reading.")
        return cleaned_data
