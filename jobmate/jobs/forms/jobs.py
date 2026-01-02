from django import forms
from jobs.models import Job
from django.contrib.auth import get_user_model

# This form allows users to edit their Profile information using model form


User = get_user_model()

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
            'tenant_name',
            'tenant_phone',
            'tenant_email',
            'priority',
            'category',
            'status',
            'description',
            'due_date',
            'estimated_hours',
            'job_cost',
            'assigned_operative'
        ]

        # Displays the input styles to match bootstrap
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'Enter job title'}),
            'property_owner': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'Property owner name'}),
            'address': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'Enter full address'}),
            'city': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'City'}),
            'post_code': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'Postcode'}),
            
            'tenant_name': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'Name'}),
            'tenant_phone': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'Phone'}),
            'tenant_email': forms.TextInput(attrs={'class': 'form-control input', 'placeholder': 'Email'}),

            'priority': forms.Select(attrs={'class': 'form-select input'}),
            'category': forms.Select(attrs={'class': 'form-select input'}),
            'status': forms.Select(attrs={'class': 'form-select input', 'name': 'status_term'}),

            'description': forms.Textarea(attrs={'class': 'form-control input', 'rows': 4, 'placeholder': 'Job description (min 20 characters)'}),

            'due_date': forms.DateInput(attrs={'class': 'form-control input', 'type': 'date'}),

            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control input', 'placeholder': 'Estimated hours'}),
            'job_cost': forms.NumberInput(attrs={'class': 'form-control input', 'placeholder': 'Job cost (£)'}),

            'assigned_operative': forms.Select(attrs={'class': 'form-select input'}),
        }

    # This function displays the users as first last names and role in the drop down list
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get all user profiles, exclude admin and sort by username
        self.fields['assigned_operative'].queryset = (
            User.objects
            .select_related('profile')
            .exclude(profile__role='Admin')
            .order_by('profile__role')
        )

        # Change the list so it displays first last names with roles except admin, if we dont use this then list will only show username
        self.fields['assigned_operative'].label_from_instance = (
            lambda user: f"{user.first_name} {user.last_name} ({user.profile.get_role_display()})"
        )