from allauth.account.forms import ResetPasswordForm as ResetForm
from urllib3 import request

# Reset form stylying for bootstrap
class CustomResetForm(ResetForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['email'].widget.attrs.update({
        "class": "form-control input",
        "placeholder": "Enter your email",
      })    