from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

# Create your tests here.

# This test checks for password reset

# CREATE USER MODEL INSTANCE
User = get_user_model()

class PasswordResetTest(TestCase):

    # SETUP USER FOR PASSWORD RESET
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass123!",
        )

    #  RESET PASSWORD 
    def test_password_reset(self):

        # Check if reset page loads and fill in the fields
        url = reverse("account_reset_password")

        # Submit reset form
        self.client.post(url, {"email": self.user.email})

        # Check if email sent
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body

        # Extract reset URL from email
        reset_url = self._extract_reset_link(email_body)

        # Open the reset link form sent in email
        response = self.client.get(reset_url, follow=True)
        # Password reset form page should load correctly
        self.assertEqual(response.status_code, 200)

        # Extract final form URL
        form_url = response.request["PATH_INFO"]

        # Submit new password
        response = self.client.post(
            # Enter new password
            form_url,
            {
                "password1": "NewPassword123!",
                "password2": "NewPassword123!",
            },
            # If form sucessful, should redirect
            follow=True
        )

        # Should redirect on success to login page
        self.assertEqual(response.status_code, 200)

        # Login using new password
        login_ok = self.client.login(
            username=self.user.username,  
            password="NewPassword123!"
        )
        print("Logged in with new password:", login_ok) 
        self.assertTrue(login_ok, "Login with new password failed!")


    #   EMAIL RESET LINK HELPER FUNCTION
    def _extract_reset_link(self, email_body):
        
        # Split the entire email text into separate lines
        lines = email_body.split("\n")

        # Look through every line and keep only the ones that contain the phrase "password/reset/key", which identifies the reset URL
        matching_lines = [
            line.strip()
            for line in lines
            if "password/reset/key" in line
        ]

        # If we found no matching line, the test should fail
        self.assertTrue(
         matching_lines,
            f"No password reset link found in email.\nEmail contents:\n{email_body}"
        )

        # Take the first matching line
        line = matching_lines[0]

        # The email may contain extra text around the URL, extract the URL beginning with http:// or https://.
        if "http://" in line:
            return line[line.index("http://"):].strip()

        if "https://" in line:
            return line[line.index("https://"):].strip()
        # If none found, return the entire line
        return line.strip()
    
