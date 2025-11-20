from django.shortcuts import render
from urllib3 import request

# Create your views here.

def payments(request):
    """
    This view renders the all payments page
    """
    return render(request, 'payments.html')

def basket(request):
    """
    This view renders the basket page
    """
    return render(request, 'basket.html')   

def job_adjustment(request):
    """
    This view renders the job adjustment page
    """
    return render(request, 'job_adjustment.html')