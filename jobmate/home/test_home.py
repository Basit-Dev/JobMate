from django.test import TestCase
from django.urls import reverse

# Create your tests here.

# This test ensures that all users can access the home page.

# TEST THAT HOME PAGE LAODS
class PageAccessTest(TestCase): 
    def test_home_page_loads(self):
        """
        The home page should open normally.
        """
        url = reverse("home:home")
        response = self.client.get(url)
        print(f"Accessing {response}, Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 200)