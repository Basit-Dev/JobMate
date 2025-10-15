from django.shortcuts import render

# Create your views here.

def create_account(request):
    """
    This view renders the create account page
    """
    return render(request, 'create_account.html')

def sign_in(request):
    """
    This view renders the sign in page
    """
    return render(request, 'sign_in.html')