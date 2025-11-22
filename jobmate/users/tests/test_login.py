from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()

# LOGIN TESTS
class LoginTest(TestCase):

    #   SETUP USER FOR LOGIN TESTS
    def setUp(self):
        self.user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="Testpass123!"
)
    
    # TEST LOGIN PAGE LOADS WITH ALL FIELDS
    def test_login_page_loads(self):
        """
        The login page should open normally.
        """
        url = reverse("account_login")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "login")
        self.assertContains(response, "password")

    #   TEST LOGIN WITH DATA
    def test_successful_login(self):
        """
        If we send correct details, User should be able to log in.
        """
        url = reverse("account_login")
        data = {
            "login": self.user.email,
            "password": "Testpass123!", # Must use RAW password here as hashed password is stored in User model
        }

        # Submit login form
        response = self.client.post(url, data)

        # After login redirect after success
        self.assertEqual(response.status_code, 302)

  #   TEST PASSWORD MISMATCH
    def test_password_mismatch(self):
        """
        If passwords do not match, signup should fail.
        """
        url = reverse("account_login")
        data = {
            "login": self.user.email,
            "password": "WrongPass",
        }

         # Submit login form
        response = self.client.post(url, data)

        # Should stay on same page (no redirect)
        self.assertEqual(response.status_code, 200)