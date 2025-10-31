from django.shortcuts import render
from urllib3 import request

# Create your views here.

def payments(request):
    """
    This view renders the all payments page
    """
    return render(request, 'payments.html')