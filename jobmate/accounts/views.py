from django.shortcuts import render

# Create your views here.

def create_account(request):
    """
    This view renders the create account page
    """
    return render(request, 'create_account.html')