from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from jobs.models import Job

# Create your tests here.

# This test ensures that a job can be created and allocated to a engineer.
# The view would be tested manually

# Command to test
# python manage.py test jobs.tests.test_create_job --verbosity 2

User = get_user_model()

class JobModelTest(TestCase):
        
    # SETUP ENGINEER TO ALLOCATE JOB
    def setUp(self):
        self.engineer = User.objects.create_user(
            username="engineer1",
        )

    # Create a job
    def test_create_job(self):
        job = Job.objects.create(
            job_title="Boiler Service",
            property_owner="John Smith",
            address="123 High Street",
            city="Cardiff",
            post_code="CF10 1AA",
            priority="medium",
            category="heating",
            status="pending",
            description="Annual boiler service required",
            due_date=date.today(),
            estimated_hours=2.5,
            job_cost=120.00,
            assigned_engineer=self.engineer,
        )

        # Check the count has gone up
        self.assertEqual(Job.objects.count(), 1)
        # Check if job title matches
        self.assertEqual(job.job_title, "Boiler Service")
        # Check if engineer matches
        self.assertEqual(job.assigned_engineer.username, "engineer1")
