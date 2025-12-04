from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.forms.profile import ProfileForm

# Create your views here.

def logged_out(request):
    """
    This view renders the logged out page
    """
    return render(request, 'logged_out.html')

@login_required
def all_engineers(request):
    """
    This view renders the all engineers page
    """
    return render(request, 'all_engineers.html')

@login_required
def profile_settings(request):
    # Get looged in user profile
    profile = request.user.profile

    # When form sent validate and save and redirect to profile page
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile_settings')
        # If not POST data use the existing data
    else:
        form = ProfileForm(instance=profile)
    print(request.POST) 
    # Render the page
    return render(request, 'profile_settings.html', {'form': form})