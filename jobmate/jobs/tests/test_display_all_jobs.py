from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from jobs.models import Job

# Create your tests here.

# This test ensures that a all jobs are displayed.
# The view would be tested manually

# Command to test
# python manage.py test jobs.tests.test_display_all_jobs --verbosity 2

User = get_user_model()

class JobDisplayAllTest(TestCase):

    # SETUP ENGINEER 
    def setUp(self):
        self.engineer = User.objects.create_user(
            username="engineer1",
        )

        # Create job 1
        Job.objects.create(
            job_title="Boiler Service",
            property_owner="John Smith",
            address="123 High Street",
            city="Cardiff",
            post_code="CF10 1AA",
            category="heating",
            description="Annual service",
            due_date=date.today(),
            assigned_engineer=self.engineer,
        )

        # Create job 2
        Job.objects.create(
            job_title="Gas Safety Check",
            property_owner="Sarah Jones",
            address="456 Queen Street",
            city="Cardiff",
            post_code="CF11 2BB",
            category="heating",
            description="Landlord safety check",
            due_date=date.today(),
        )

    # Get all jobs
    def test_load_all_jobs(self):
        jobs = Job.objects.all()

        # Does job count = to jobs created above
        self.assertEqual(jobs.count(), 2)