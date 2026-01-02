from allauth.account.forms import LoginForm

  
# Login form stylying
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['login'].widget.attrs.update({
          "class": "form-control",
          "placeholder": "Enter your email",
          })
      self.fields['password'].widget.attrs.update({
          "class": "form-control",
          "placeholder": "Enter your password",
          })
      
