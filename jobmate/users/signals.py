from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# We will use Signals so that when user is created or deleted it is synced

# Automatically create a Profile when a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # 'created' = True only the FIRST time a user is saved
    if created:
        # Create a Profile linked to this user
        Profile.objects.create(user=instance)

# Automatically save the Profile whenever the User is saved so user and profile in sync
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()