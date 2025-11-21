from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from urllib3 import request

# Create your views here.

@login_required
def payments(request):
    """
    This view renders the all payments page
    """
    return render(request, 'payments.html')

@login_required
def basket(request):
    """
    This view renders the basket page
    """
    return render(request, 'basket.html')   

@login_required
def job_adjustment(request):
    """
    This view renders the job adjustment page
    """
    return render(request, 'job_adjustment.html')