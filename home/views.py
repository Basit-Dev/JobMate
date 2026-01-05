from django.shortcuts import render

# Create your views here.

def home(request):
    """
    This view renders the home page
    """
    return render(request, "home.html", {"hide_footer": True})