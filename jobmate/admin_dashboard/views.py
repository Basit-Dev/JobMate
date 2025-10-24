from django.shortcuts import render

# Create your views here.

def all_jobs(request):
    """
    This view renders the all jobs page
    """
    return render(request, 'all_jobs.html')  

def engineers(request):
    """
    This view renders the engineers page
    """
    return render(request, 'engineers.html')