from django import forms
from users.models import Profile

# This form allows users to edit their Profile information using model form

class ProfileForm(forms.ModelForm):

    class Meta:
        # Profile fields
        model = Profile
        fields = [
            'phone_number',
            'role',
            'bank_name',
            'account_holder',
            'account_number',
            'sort_code',
        ]
        # Displays the input styles to match bootstrap
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_holder': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sort_code': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control',  'readonly': 'readonly'}), 
        }