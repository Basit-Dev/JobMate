from django import forms
from cart.models import Orders
from django.contrib.auth import get_user_model

# This form allows users to edit their Profile information using model form

User = get_user_model()

class PaymentForm(forms.ModelForm):

    class Meta:
        # Payment fields
        model = Orders
        fields = [
            'status',
        ]

        # Displays the input styles to match bootstrap
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select input', 'name': 'status_term'}),
        }