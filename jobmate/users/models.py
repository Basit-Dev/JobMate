from django.db import models
from django.contrib.auth.models import User


# Profile model: this stores extra information about users on top of django built in model

class Profile(models.Model):

    # User roles to be added on production version
    # ROLE_CHOICES = [
    #     ('admin', 'Admin'),
    #     ('engineer', 'Engineer'),
    # ]

    # 1 to 1 relationship link to extend Djangos user model: each User gets exactly one Profile that links with Django allauth User.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile fields
    phone_number = models.CharField(
        max_length=20,
        blank=False,   
    )

    role = models.CharField(
        max_length=20,
        # choices=ROLE_CHOICES,  To be added later
        default='Engineer'     
    )

    # Bank details
    bank_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    account_holder = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    account_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    sort_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # This displays the profile name in the admin and shell
    def __str__(self):
        return f"{self.user.username} Profile"