from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile

# Create your tests here.

# This test checks the profile details

# Command to test
# python manage.py test users.tests.test_profile --verbosity 2

User = get_user_model()

class ProfileTest(TestCase):

    # SETUP USER FOR ALL TESTS
    def setUp(self):
        # Create a test user note Django auto-creates a Profile via signals
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass123!",
            first_name="John",
            last_name="Doe",
        )

        # URL for the profile settings page
        self.url = reverse("users:profile_settings")

    # Test profile page loads for a logged in user
    def test_profile_page_loads_for_logged_in_user(self):
        """
        Logged in users should be able to load the profile settings page
        """

        # Login with credentials
        self.client.login(username="testuser", password="Testpass123!")
        response = self.client.get(self.url)

        # Success 200
        self.assertEqual(response.status_code, 200)

    # Test user info loads correctly
    def test_user_profile_displays(self):

        """
        Logged in users should be able to view profile settings
        """

        # Log in
        self.client.login(username="testuser", password="Testpass123!")

        # Check if data matches
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")

    # Test personal info form saves and loads correctly
    def test_personal_info_saves(self):
        """
        Submitting the personal info form should update User and Profile models
        """
        self.client.login(username="testuser", password="Testpass123!")

        data = {
            "submit_personal": "1",
            "phone_number": "12345678",
            "role": "Engineer",
        }

        # Sumbit form
        response = self.client.post(self.url, data)
        # After signup redirect after success
        self.assertEqual(response.status_code, 302)

        # Refresh DB
        self.user.refresh_from_db()
        profile = Profile.objects.get(user=self.user)

        # Check if profile has updated
        self.assertEqual(profile.phone_number, "12345678")
        self.assertEqual(profile.role, "Engineer")

    # Test bank details form saves correctly
    def test_bank_details_saves(self):
        """
        Submitting the bank details form should update Profile bank fields.
        """
        self.client.login(username="testuser", password="Testpass123!")

        # Bank data
        data = {
            "submit_bank": "1",
            "bank_name": "HSBC",
            "account_holder": "Joe Doe",
            "account_number": "555",
            "sort_code": "12-34-56",
        }

        # Sumbit form
        response = self.client.post(self.url, data)
        # After signup redirect after success
        self.assertEqual(response.status_code, 302)

        # Get profile
        profile = Profile.objects.get(user=self.user)

        # Check profile bank details match
        self.assertEqual(profile.bank_name, "HSBC")
        self.assertEqual(profile.account_holder, "Joe Doe")
        self.assertEqual(profile.account_number, "555")
        self.assertEqual(profile.sort_code, "12-34-56")

    # Test password change works
    def test_password_can_be_changed(self):
        """
        Submitting the password form should update the user's password.
        """

        # Log in with credentials
        self.client.login(username="testuser", password="Testpass123!")

        # Password data
        data = {
            "submit_password": "1",
            "old_password": "Testpass123!",
            "new_password1": "NewPass123!",
            "new_password2": "NewPass123!",
        }

        response = self.client.post(self.url, data)

        # Should redirect after successful password change
        self.assertEqual(response.status_code, 302)

        # Verify new password works
        login_ok = self.client.login(username="testuser", password="NewPass123!")
        self.assertTrue(login_ok)