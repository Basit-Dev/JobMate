from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from jobs.forms.jobs import JobForm
from django.contrib import messages
from django.db.models import Q

# Create your views here.


@login_required
def all_jobs(request):
    """
    This view renders the all jobs page
    """
    # Get current logged in User
    user = request.user

    # Get the search term from all_jobs search box when user presses search button
    user_query = request.GET.get("search_term")

    # If user is engineer display related to assigned user jobs else display all the jobs
    if user.profile.role == "Engineer":

        # If user entered a query render filtered jobs else get user assigned jobs
        if user_query:
            filtered_job_list = Job.objects.filter(assigned_engineer=user).filter(Q(job_title__icontains=user_query) | Q(
                address__icontains=user_query) | Q(city__icontains=user_query) | Q(post_code__icontains=user_query))
            return render(request, 'all_jobs.html', {"job_list": filtered_job_list})
        else:
            job_list = Job.objects.filter(assigned_engineer=user)

    # If admin entered a query render filtered jobs else get all jobs
    else:
        if user_query:
            filtered_job_list = Job.objects.filter(Q(job_title__icontains=user_query) | Q(
                address__icontains=user_query) | Q(city__icontains=user_query) | Q(post_code__icontains=user_query))
            return render(request, 'all_jobs.html', {"job_list": filtered_job_list})
        else:
            job_list = Job.objects.all()
    # If no search query entered render jobs based on role
    return render(request, 'all_jobs.html', {"job_list": job_list})


@login_required
def edit_job(request):
    """
    This view renders the edit job page
    """
    return render(request, 'edit_job.html')


@login_required
def job_detail(request):
    """
    This view renders the job detail page
    """
    return render(request, 'job_detail.html')


@login_required
def delete_job(request):
    """
    This view renders the delete job page
    """
    return render(request, 'delete_job.html')

# CREATE NEW JOB


@login_required
def create_job(request):

    # POST JOB INFO
    if request.method == "POST":
        create_job_form = JobForm(request.POST)

        if create_job_form.is_valid():
            job = create_job_form.save(commit=False)
            job.created_by = request.user   # attach the user
            job.save()
            create_job_form.save()
            messages.success(request, 'Job was successfully created!')
            return redirect("jobs:all_jobs")
        else:
            # Show error messages
            messages.error(request, "Please correct the errors below.")

    # If NOT posting data then load the value from the JobForm
    else:
        create_job_form = JobForm()

    # Load the profile page on request and pass the data to the forms on render
    return render(request, "create_job.html", {"create_job_form": create_job_form})
