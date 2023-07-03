from django import forms
from .models import tenant

class TenantSignUpForm(forms.ModelForm):
    class Meta:
        model = tenant
        fields = ('First_name', 'Second_name', 'Phone_number', 'email', 'ID_number', 'ID_front', 'ID_back', 'Signed_contract')
        widgets = {
            'First_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ID_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ID_front': forms.FileInput(attrs={'class': 'form-control-file'}),
            'ID_back': forms.FileInput(attrs={'class': 'form-control-file'}),
            'Signed_contract': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_Phone_number(self):
        phone_number = self.cleaned_data['Phone_number']
        if len(phone_number) != 10:
            raise forms.ValidationError("Please enter a valid phone number, format = 0XXXXXXXXXX")
        return phone_number