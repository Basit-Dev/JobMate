from django import forms
from jobs.models import Job

# This form allows users to edit their Profile information using model form

class JobForm(forms.ModelForm):

    class Meta:
        # Job fields
        model = Job
        fields = [
            'job_title',
            'property_owner',
            'address',
            'city',
            'post_code',
            'priority',
            'category',
            'status',
            'description',
            'due_date',
            'estimated_hours',
            'job_cost',
            'assigned_engineer'
        ]

        # Displays the input styles to match bootstrap
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'property_owner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property owner name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'post_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'}),

            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),

            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Job description (min 20 characters)'}),

            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated hours'}),
            'job_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Job cost (£)'}),

            'assigned_engineer': forms.Select(attrs={'class': 'form-select'}),
        }
