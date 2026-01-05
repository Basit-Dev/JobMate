from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

# This test ensures that only registered users can access certain pages, and that public pages are accessible to all users.

# Command to test
# python manage.py test jobs.tests.test_job_pages_access --verbosity 2

User = get_user_model()

class JobPagesAccessTest(TestCase):

    # SETUP USER FOR TO TEST ACCESS
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass123!",
        )

    # TEST THAT UNREGISTERED USERS CANNOT ACCESS PROTECTED URL PAGES
    def test_protected_page_redirects(self):
        protected_urls = [
            reverse("jobs:all_jobs"),
            reverse("jobs:create_job"),
            reverse("jobs:delete_job"),
            reverse("jobs:edit_job"),
            reverse("jobs:job_detail"),
        ]

        # Loop through protected URLs and redirect to login page for unregistered users
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("account_login"), response.url)

    # TEST THAT REGISTERED USERS CAN ACCESS PROTECTED PAGES
    def test_protected_page_access(self):

        # Login the user
        login_ok = self.client.login(
            username=self.user.username,
            password="Testpass123!"
        )
        print("Login successful:", login_ok)
        self.assertTrue(login_ok, "Login failed for test user")

        protected_urls = [
            reverse("jobs:all_jobs"),
            reverse("jobs:create_job"),
            reverse("jobs:delete_job"),
            reverse("jobs:edit_job"),
            reverse("jobs:job_detail"),
        ]

        # Loop through protected URLs and check if page loads
        for url in protected_urls:
            response = self.client.get(url)
            # If login page displayed, access failed
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, reverse("account_login"))
            print(f"Accessing {url}, Status Code: {response.status_code}")
        # Logout the user after tests
        self.client.logout()

    # TEST THAT PUBLIC PAGES ARE ACCESSIBLE WITHOUT LOGIN
    def test_public_pages(self):
        public_urls = [
            reverse("account_login"),
            reverse("account_signup"),
            reverse("account_reset_password"),
            reverse("account_reset_password_done"),
        ]

        # Loop through public URLs and check if page loads
        for url in public_urls:
            response = self.client.get(url)
            print(f"Accessing {url}, Status Code: {response.status_code}")
            self.assertEqual(response.status_code, 200)