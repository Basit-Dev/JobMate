from django.shortcuts import render

# Create your views here.

def home(request):
    """
    This view renders the landing page
    """
    return render(request, 'home.html')