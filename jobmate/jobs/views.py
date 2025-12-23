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

    # Get the search term from search box or status filter
    search_query = request.GET.get("search_term")
    status_filter = request.GET.get("status_filter")

    # If user is engineer display assigned engineer jobs else display all the jobs in job_list variable
    if user.profile.role == "Engineer":
        job_list = Job.objects.filter(assigned_engineer=user)
    else:
        job_list = Job.objects.all()

    # If search query then filter the existing job_list variable mutate it and give the results
    if search_query:
        job_list = job_list.filter(
            Q(job_title__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(post_code__icontains=search_query))

    # If status query then filter the existing job_list variable mutate it and give the results
    if status_filter:
        job_list = job_list.filter(status=status_filter)

    # Finally render job list based on above conditions
    return render(request, 'all_jobs.html', {"job_list": job_list})


@login_required
def edit_job(request, job_id):
    """
    This view renders the edit job page
    """

    # Get current logged in User
    user = request.user

    # Get the job ID
    job = Job.objects.get(pk=job_id)

    # If post request save the new data using the job instance else GET the job instace as a form with existing data
    if request.method == "POST":
        job_edit_form = JobForm(request.POST, instance=job)
        if job_edit_form.is_valid():
            job_edit_form.save()
            messages.success(request, 'Job details was successfully updated!')
            return redirect("jobs:all_jobs")
    else:
        job_edit_form = JobForm(instance=job)

    # Admins can only have access to editing job
    if user.profile.role == "Admin":
        return render(request, "edit_job.html", {"job_edit_form": job_edit_form})

    # Anyone other than admin cant view urls or the jobs to edit and get redirected to all_jobs page
    return render(request, 'all_jobs.html')


@login_required
def job_detail(request, job_id):
    """
    This view renders the job detail page
    """
    # Get current logged in User
    user = request.user

    # Get the job ID
    job = Job.objects.get(pk=job_id)

    # Admins can view all jobs
    if user.profile.role == "Admin":
        return render(request, "job_detail.html", {"job": job})

    # Only assigned engineer can view their job
    if job.assigned_engineer == user:
        return render(request, "job_detail.html", {"job": job})

    # Else render the all jobs page showing the no jobs found message
    return render(request, 'all_jobs.html')


@login_required
def delete_job(request, job_id):
    """
    This view renders the delete job page
    """
    # Get current logged in User
    user = request.user

    # If admin tsends a post request, form is submitted, get the job id, delete job, show message, redirect to all jobs
    # Otherwise if job does not exit then redirect to all jobs and show message
    if user.profile.role == "Admin":
        try:
            job = Job.objects.get(pk=job_id)
            if request.method == "POST":
                job.delete()
                messages.success(request, 'Job details was successfully deleted!')
                return redirect("jobs:all_jobs")
            return render(request, "delete_job.html", {"job": job})
        except Job.DoesNotExist:
            messages.success(request, 'Does Not Exist!')
            return redirect("jobs:all_jobs")
        # If NOT admin then show message and redirect to all jobs
    else: 
        messages.success(request, 'Does Not Exist!')
        return redirect("jobs:all_jobs")


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
