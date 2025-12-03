from allauth.account.forms import SignupForm
from django import forms

# Signup form
class CustomSignupForm(SignupForm):
  
#   Custom fileds with Bootstrap classes
  first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        required=True
    )
  last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
,       required=True
    )
  email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        required=True
    )
  
  ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Engineer', 'Engineer'),
    ]
  
  role = forms.ChoiceField(
      choices=ROLE_CHOICES, label='Role',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
  
#   Customize password fields to match Bootstrap
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
    })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
    }) 
  
#   Save data on submit
  def save(self, request):
        user = super().save(request)

        # Save user fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        # Save role fields into profile settings
        user.profile.role = self.cleaned_data['role'] 
        user.profile.save()

        return user