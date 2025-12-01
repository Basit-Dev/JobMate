from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

# This test checks for user signup

User = get_user_model()

# SIGNUP TESTS
class SignupTest(TestCase):
    
    # TEST SIGNUP PAGE LOADS WITH ALL FIELDS
    def test_signup_page_loads(self):
        """
        The signup page should open normally.
        """
        url = reverse("account_signup")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "role")
        self.assertContains(response, "email")
        self.assertContains(response, "password1")
        self.assertContains(response, "password2")

    #   TEST SIGNUP WITH DATA
    def test_successful_signup(self):
        """
        If we send correct details, a new user should be created.
        """
        url = reverse("account_signup")
        data = {
            "first_name": "Test",
            "last_name": "User",
            "role": "engineer",
            "email": "test@example.com",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
        }

        # Submit signup form
        response = self.client.post(url, data)

        # After signup check if user exists in the database
        user_exists = User.objects.filter(email="test@example.com").exists()
        self.assertTrue(user_exists)

        # After signup redirect after success
        self.assertEqual(response.status_code, 302)

    #   TEST PASSWORD MISMATCH
    def test_password_mismatch(self):
        """
        If passwords do not match, signup should fail.
        """
        url = reverse("account_signup")
        data = {
            "first_name": "Test",
            "last_name": "User",
            "role": "engineer",
            "email": "test@example.com",
            "password1": "Testpass123!",
            "password2": "WrongPass",
        }

         # Submit signup form
        response = self.client.post(url, data)

        # Should stay on same page (no redirect)
        self.assertEqual(response.status_code, 200)

        # No user should be created
        user_exists = User.objects.filter(email="test2@example.com").exists()
        self.assertFalse(user_exists)    
