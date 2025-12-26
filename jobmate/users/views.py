from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.forms.profile import ProfileForm, BankDetailsForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import get_user_model 
from django.db.models import Q
from helpers.permission_check import admin_required

# Create your views here.

# NOTE: The PERSONAL_FORM is in two parts 1 is the User and the other is the Profile
# USER FIELDS: first_name, last_name, email_address and user_name. To get a value use profile_owner.first_name etc
# PROFILE FIELDS: phone_number, role, and status. To get a value use personal_form.role etc

User = get_user_model()

# LOGGED OUT
def logged_out(request):
    """
    This view renders the logged out page
    """
    return render(request, 'logged_out.html')

# ALL ENGINEERS
@login_required
@admin_required
def all_operatives(request):
    """
    This view renders the all engineers page
    """
    # Get the search term
    search_query = request.GET.get("search_operatives")

    # Get all engineers from user model
    operative_list = get_user_model().objects.all()
    
    # Remove admins from the list
    operative_list = operative_list.exclude(profile__role="Admin")
    
    # If search query submits form then filter the engineers and update operative_list  
    if search_query:
        # As the role list is defined by gas_engineer, this line is saying remove and replace the space from search query with _
        full_query = search_query.replace(" ", "_") 
        operative_list = operative_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(profile__role__icontains=full_query) |
            Q(profile__status__icontains=search_query))
        
    # Finally render engineers based on above conditions
    return render(request, 'all_operatives.html', {'operative_list': operative_list})

# PROFILE SETTINGS
@login_required
def profile_settings(request, profile_id=None):
    """
    This view renders the profile settings page
    """  
     # Get logged-in user's profile
    profile_owner = request.user
    
    # If admin is trying to view another user get the id if it exists else show error 404, message and redirect to user profile
    if profile_id is not None:
        if request.user.profile.role != "Admin":
            messages.error(request, "You do not have permission to view this profile.")
            return redirect("users:profile_settings")

        # Get Profile for give profile_id
        profile_owner = get_object_or_404(User, id=profile_id)

    # If the user is the logged in and clicks profile then their profile will be shown as no ID has been passed
    profile = profile_owner.profile

    # POST PERSONAL INFO
    if request.method == "POST" and "submit_personal" in request.POST:
        personal_form = ProfileForm(request.POST, instance=profile)
        bank_form = BankDetailsForm(instance=profile)
        password_form = PasswordChangeForm(request.user)
        print(profile.status)

        if personal_form.is_valid():
            print(personal_form.cleaned_data["status"])
            personal_form.save()
            print("saved")
            messages.success(request, 'Your profile was successfully updated!')
            if request.user.profile.role != "Admin":
                return redirect("users:profile_settings")
            else:
                return redirect("users:all_engineers") # If admin updates profile then stay on the same profile id page

    # POST BANK DETAILS
    elif request.method == "POST" and "submit_bank" in request.POST:
        bank_form = BankDetailsForm(request.POST, instance=profile)

        if bank_form.is_valid():
            bank_form.save()
            messages.success(request, 'Your bank details was successfully updated!')
            if request.user.profile.role != "Admin":
                return redirect("users:profile_settings")
            else: 
                return redirect("users:profile_settings", profile_id=profile_owner.id) # If admin updates profile then stay on the same profile id page

    # POST PASSWORD
    elif request.method == "POST" and "submit_password" in request.POST:
        personal_form = ProfileForm(instance=profile)
        bank_form = BankDetailsForm(instance=profile)
        password_form = PasswordChangeForm(request.user, request.POST)

        # Keep bootstrap styling for the password input fields the same when POST data then redirects
        for field in password_form.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = ""

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            if request.user.profile.role != "Admin":
                return redirect("users:profile_settings")
            else:
                return redirect("users:profile_settings", profile_id=profile_owner.id) # If admin updates profile then stay on the same profile id page
            
    # If NOT posting data then load the value from the instance
    else:
        personal_form = ProfileForm(instance=profile)
        bank_form = BankDetailsForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

        # Bootstrap styling for the password input fields
        for field in password_form.fields.values():
            field.widget.attrs["class"] = "form-control input"
            field.widget.attrs["placeholder"] = ""
            field.widget.attrs.pop("autofocus", None) # Remove focus when the profile page loads

    # Load the profile page on request and pass the data to the forms on render
    return render(
        request,
        "profile_settings.html",
        {
            "personal_form": personal_form,
            "bank_form": bank_form,
            "password_form": password_form,
            "profile_owner": profile_owner, # We need profile_owner for the admin to access the USER FIELDS
        },
    )
    
    
@login_required
@admin_required
def delete_operative(request, profile_id=None):
    """
    This view renders the delete engineer page
    """

    # Get the profile id if it doesnt exist return 404
    operative = get_object_or_404(User, pk=profile_id)

    # Admin sends a post request, form is submitted, get the profile id, delete job, show message, redirect to all engineers
    if request.method == "POST":
        operative.delete()
        messages.success(request, "Engineer deleted successfully.")
        return redirect("users:all_engineers")

    return render(request, "delete_operative.html", {"operative": operative})
