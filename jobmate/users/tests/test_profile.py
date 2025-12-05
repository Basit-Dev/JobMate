from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile

# Create your tests here.

# This test checks the profile details

# Command to test
# python manage.py test users.tests.test_profile --verbosity 2

User = get_user_model()

# PROFILE TESTS
class ProfileTest(TestCase):

    # SETUP USER FOR LOGIN TESTS
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass123!"
        )

        #  Once profile is setup go to the prifle settings page
        self.url = reverse("users:profile_settings")

    # Test profile page loads once user is logged in
    def test_profile_page_loads_for_logged_in_user(self):
        """
        Logged-in user can load the profile settings page.
        """
        self.client.login(username="testuser", password="Testpass123!")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    # Post new data
    def test_profile_saves_new_data(self):
        """
        Submitting the profile form should update the users profile
        """
        self.client.login(username="testuser", password="Testpass123!")

        # New data
        data = {
            "form_type": "personal",
            "phone_number": "12345678",
            "role": "engineer",  
            "bank_name": "HSBC",
            "account_holder": "Joe Doe",
            "account_number": "12345678",
            "sort_code": "12-34-56",
        }

        # Post form
        response = self.client.post(self.url, data)

        # Should redirect back to settings
        self.assertEqual(response.status_code, 302)

        # Refresh and get profile from database
        profile = Profile.objects.get(user=self.user)

        # Check if new data in database
        self.assertEqual(profile.phone_number, "12345678")
        self.assertEqual(profile.bank_name, "HSBC")
        self.assertEqual(profile.account_holder, "Joe Doe")
        self.assertEqual(profile.account_number, "12345678")
        self.assertEqual(profile.sort_code, "12-34-56") 
