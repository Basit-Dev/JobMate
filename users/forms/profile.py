from django import forms
from users.models import Profile

# This form allows users to edit their Profile information using model form

class ProfileForm(forms.ModelForm):

    class Meta:
        # Profile fields
        model = Profile
        fields = [
            'phone_number',
            # 'role',
            'status',
        ]

        # Displays the input styles to match bootstrap
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control input"}),
            # 'role': forms.TextInput(attrs={'class': 'form-control input',  'readonly': 'readonly'}), 
            'status': forms.Select(attrs={'class': 'form-select input', 'name': 'status_term'}),
        }
   

class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bank_name", 
            "account_holder", 
            "account_number", 
            "sort_code"
        ]

        # Displays the input styles to match bootstrap
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control input'}),
            'account_holder': forms.TextInput(attrs={'class': 'form-control input'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control input'}),
            'sort_code': forms.TextInput(attrs={'class': 'form-control input'}),
        }    