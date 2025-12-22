from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from jobs.models import Job

# Create your tests here.

# This test ensures that only admin can edit jobs, and job updates after changing original data.

# Command to test
# python manage.py test jobs.tests.test_edit_job --verbosity 2

User = get_user_model()

class TestEditJob(TestCase):

    def setUp(self):
        # CREATE ADMIN USER
        self.admin_user = User.objects.create_user(
            username="admin1",
            password="testpass123"
        )
        self.admin_user.profile.role = "admin"
        self.admin_user.profile.save()

        # CREATE A JOB
        self.job = Job.objects.create(
            job_title="Old Job Title",
            property_owner="John Smith",
            address="123 High Street",
            city="Cardiff",
            post_code="CF10 1AA",
            tenant_name="Jane",
            tenant_phone="07123456789",
            tenant_email="jane@gmail.com",
            priority="high",
            category="heating",
            status="completed",
            description="Old description",
            due_date=date.today(),
            estimated_hours=2.0,
            job_cost=120.00,
            assigned_engineer=self.admin_user,
        )

        # GO TO EDIT JOB WITH THE JOB ID
        self.url = reverse("jobs:edit_job", args=[self.job.id])

    def test_admin_can_edit_job(self):
        # LOGIN AS ADMIN
        self.client.force_login(self.admin_user)

        # SUBMIT EDITED JOB
        response = self.client.post(
            self.url,
            {
                "job_title": "Updated Job Title",
                "property_owner": "Mark Barnes",
                "address": "1 New St",
                "city": "Holesdfale",
                "post_code": "HR1 1QW",
                "tenant_name": "Paul Sykes",
                "tenant_phone": "12345678",
                "tenant_email": "ps@gmail.com",
                "priority": "low",
                "category": "plumbing",
                "status": "in_progress",
                "description": "Updated description",
                "due_date": date.today(),
                "estimated_hours": 2.5,
                "job_cost": 150.00,
            }
        )

        # Reload job from database
        self.job.refresh_from_db()

        # FORM SAVES AND REDIRECT
        self.assertEqual(response.status_code, 302)
        # HAS DATA CHANGED
        self.assertEqual(self.job.job_title, "Updated Job Title")
        self.assertEqual(self.job.description, "Updated description")
        self.assertEqual(self.job.job_cost, 150.00)