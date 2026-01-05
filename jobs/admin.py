from django.contrib import admin
from .models import Job

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job_title",
        "status",
        "created_at",
        "completed_at",
        "assigned_operative",
    )

    readonly_fields = (
        "completed_at",
    )

    fields = (
        "job_title",
        "property_owner",
        "address",
        "city",
        "post_code",
        "tenant_name",
        "tenant_phone",
        "tenant_email",
        "priority",
        "category",
        "status",
        "description",
        "due_date",
        "completed_at",
        "estimated_hours",
        "job_cost",
        "assigned_operative",
    )