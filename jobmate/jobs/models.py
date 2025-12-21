from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    # Priority options
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    # Category options
    CATEGORY_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('heating', 'Heating'),
        ('electrical', 'Electrical'),
    ]

    # Status options
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    # Job details
    job_title = models.CharField(max_length=100)
    property_owner = models.CharField(max_length=100)

    # Property address
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    
    # Tenant details
    tenant_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    tenant_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    tenant_email = models.EmailField(
        max_length=254,
        null=True,
        blank=True
    )

    # Priority and category
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    # Job status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # Description
    description = models.TextField()  
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField()

    # Hours and cost
    estimated_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )

    job_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Engineer assignment
    assigned_engineer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs"
    )

    def __str__(self):
        return f"{self.job_title} - {self.property_owner}"
