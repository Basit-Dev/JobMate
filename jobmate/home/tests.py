from django.test import TestCase

# Create your tests here.

# This test ensures that all users can access the home page.

  # TEST THAT PUBLIC PAGES ARE ACCESSIBLE WITHOUT LOGIN
def test_home_page(self):

            response = self.client.get("home")
            print(f"Accessing {response}, Status Code: {response.status_code}")
            self.assertEqual(response.status_code, 200)