from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

# This test ensures that only registered users can access shopping cart pages.

# Command to test
# python manage.py test cart.tests.test_cart_pages_access --verbosity 2

User = get_user_model()

class CartPagesAccessTest(TestCase):

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
            reverse("cart:basket"),
            reverse("cart:job_adjustment"),
            reverse("cart:payments"),
        ]

        # Loop through protected URLs and redirect to login page for unregistered users
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("account_login"), response.url)
            print(f"Access Denied {url}, Status Code: {response.status_code}")

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
            reverse("cart:basket"),
            reverse("cart:job_adjustment"),
            reverse("cart:payments"),
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