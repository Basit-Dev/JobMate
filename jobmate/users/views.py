from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.forms.profile import ProfileForm, BankDetailsForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.

# LOGGED OUT
def logged_out(request):
    """
    This view renders the logged out page
    """
    return render(request, 'logged_out.html')

# ALL ENGINEERS
@login_required
def all_engineers(request):
    """
    This view renders the all engineers page
    """
    return render(request, 'all_engineers.html')

# PROFILE SETTINGS
@login_required
def profile_settings(request):
    profile = request.user.profile

    # POST PERSONAL INFO
    if request.method == "POST" and "submit_personal" in request.POST:
        personal_form = ProfileForm(request.POST, instance=profile)
        bank_form = BankDetailsForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

        if personal_form.is_valid():
            personal_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect("users:profile_settings")

    # POST BANK DETAILS
    elif request.method == "POST" and "submit_bank" in request.POST:
        bank_form = BankDetailsForm(request.POST, instance=profile)

        if bank_form.is_valid():
            bank_form.save()
            messages.success(request, 'Your bank details was successfully updated!')
            return redirect("users:profile_settings")

    # POST PASSWORD
    elif request.method == "POST" and "submit_password" in request.POST:
        personal_form = ProfileForm(instance=profile)
        bank_form = BankDetailsForm(instance=profile)
        password_form = PasswordChangeForm(request.user, request.POST)

        # Keep bootstrap styling for the password input fields the same when POST data then redirects
        for field in password_form.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "************"

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect("users:profile_settings")
    # If NOT posting data then load the value from the instance
    else:
        personal_form = ProfileForm(instance=profile)
        bank_form = BankDetailsForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

        # Bootstrap styling for the password input fields
        for field in password_form.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "************"
            field.widget.attrs.pop("autofocus", None) # Remove focus when the profile page loads

    # Load the profile page on request and pass the data to the forms on render
    return render(
        request,
        "profile_settings.html",
        {
            "personal_form": personal_form,
            "bank_form": bank_form,
            "password_form": password_form,
        },
    )