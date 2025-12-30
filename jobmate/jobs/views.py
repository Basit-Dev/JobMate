from django.shortcuts import redirect, render, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from jobs.forms.jobs import JobForm
from django.contrib import messages
from django.db.models import Q
from helpers.permission_check import admin_required
from cart.models import Transaction
from cart.models import Transaction

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

    # If user is operative display assigned operative jobs else display all the jobs in job_list variable
    if user.profile.role != "Admin":
        job_list = Job.objects.filter(assigned_operative=user)
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
        
    # Get payment status 
    for job in job_list:
        transaction = (
            Transaction.objects
            .filter(job=job)
            .order_by("-created_at")
            .first()
        )
        job.payment_status = transaction.status if transaction else None

    # Finally render job list based on above conditions
    return render(request, 'all_jobs.html', {"job_list": job_list, "status_filter": status_filter, "search_query": search_query})


@login_required
def job_detail(request, job_id):
    """
    This view renders the job detail page
    """
    # Get current logged in User
    user = request.user

    # Get the job ID if it doesnt exist return 404
    job = get_object_or_404(Job, pk=job_id)
    
    # Permission check FIRST
    if not (
        user.profile.role == "Admin" or
        job.assigned_operative == user
    ):
        messages.error(request, "You do not have permission to view this job.")
        return redirect("jobs:all_jobs")
    
    # When job completed btn pressed change the status to completed, create a transaction, save the user who created the transaction and go to basket.html
    if request.method == "POST":
         # Prevent double completion
        if job.status == "completed":
            messages.info(request, "Job is already completed.")
            return redirect("cart:basket")

        # Mark job as completed
        job.status = "completed"
        job.save(update_fields=["status"])

        # Create OR reuse ONE open transaction
        transaction, created = Transaction.objects.get_or_create(
            job=job,
            status="open",
            defaults={
                "user": job.assigned_operative
            }
        )

        messages.success(
            request,
            "Job completed and added to basket."
            if created else
            "Job already exists in basket."
        )

        return redirect("cart:basket")
    return render(request, "job_detail.html", {"job": job})
    


@login_required
@admin_required
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


@login_required
@admin_required
def edit_job(request, job_id):
    """
    This view renders the edit job page
    """

    # Get the job ID if it doesnt exist return 404
    job = get_object_or_404(Job, pk=job_id)

    # If post request save the new data using the job instance else GET the job instace as a form with existing data
    if request.method == "POST":
        job_edit_form = JobForm(request.POST, instance=job)
        if job_edit_form.is_valid():
            job_edit_form.save()
            messages.success(request, 'Job details was successfully updated!')
            return redirect("jobs:all_jobs")
    else:
        job_edit_form = JobForm(instance=job)
    return render(request, "edit_job.html", {"job_edit_form": job_edit_form})


@login_required
@admin_required
def delete_job(request, job_id):
    """
    This view renders the delete job page
    """

    # Get the job ID if it doesnt exist return 404
    job = get_object_or_404(Job, pk=job_id)

    # Admin sends a post request, form is submitted, get the job id, delete job, show message, redirect to all jobs
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("jobs:all_jobs")

    return render(request, "delete_job.html", {"job": job})


@login_required
@admin_required
def edit_job(request, job_id):
    """
    This view renders the edit job page
    """

    # Get the job ID if it doesnt exist return 404
    job = get_object_or_404(Job, pk=job_id)

    # If post request save the new data using the job instance else GET the job instace as a form with existing data
    if request.method == "POST":
        job_edit_form = JobForm(request.POST, instance=job)
        if job_edit_form.is_valid():
            job_edit_form.save()
            messages.success(request, 'Job details was successfully updated!')
            return redirect("jobs:all_jobs")
    else:
        job_edit_form = JobForm(instance=job)
    return render(request, "edit_job.html", {"job_edit_form": job_edit_form})


@login_required
@admin_required
def delete_job(request, job_id):
    """
    This view renders the delete job page
    """

    # Get the job ID if it doesnt exist return 404
    job = get_object_or_404(Job, pk=job_id)

    # Admin sends a post request, form is submitted, get the job id, delete job, show message, redirect to all jobs
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("jobs:all_jobs")

    return render(request, "delete_job.html", {"job": job})
