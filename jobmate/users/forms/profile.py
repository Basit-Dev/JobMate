from django import forms
from users.models import Profile

# This form allows users to edit their Profile information using model form

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'role',
            'bank_name',
            'account_holder',
            'account_number',
            'sort_code',
        ]