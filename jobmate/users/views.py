from django.shortcuts import render

# Create your views here.

def logged_out(request):
    """
    This view renders the logged out page
    """
    return render(request, 'logged_out.html')

def all_engineers(request):
    """
    This view renders the all engineers page
    """
    return render(request, 'all_engineers.html')

def profile_settings(request):
    """
    This view renders the profile settings page
    """
    return render(request, 'profile_settings.html')
