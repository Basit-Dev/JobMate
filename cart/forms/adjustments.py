from django import forms
from cart.models import TransactionLineItem

# This form allows users to add line items to adjustments

class AdjustmentForm(forms.ModelForm):

    class Meta:
        # Adjustment fields
        model = TransactionLineItem
        fields = [
            'description',
            'quantity',
            'unit_price',
        ]

        # Displays the input styles to match bootstrap
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control input', 'rows': 1, 'placeholder': 'Enter item description (min 20 characters)'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control input', 'placeholder': 'Qty'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control input', 'placeholder': 'Unit Price'}),
        }