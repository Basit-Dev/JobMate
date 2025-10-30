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

def create_job(request):
    """
    This view renders the create job page
    """
    return render(request, 'create_job.html')   

def edit_job(request):
    """
    This view renders the edit job page
    """
    return render(request, 'edit_job.html')

def job_details(request):
    """
    This view renders the job details page
    """
    return render(request, 'job_details.html')