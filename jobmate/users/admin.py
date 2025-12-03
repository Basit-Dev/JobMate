from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# Register your models here.

# This class allows profile fields to appear inside the user page in django admin.
class ExtraProfileFields(admin.StackedInline):
    model = Profile              # This tells Django which model to include in the admin page
    can_delete = False           # Remove delete checkbox
    extra = 0                    # Do not show any empty profile forms


# Extend django UserAdmin so we can attach our ExtraProfileFields to it.
class Profile(UserAdmin):
    inlines = [ExtraProfileFields]    # Add Profile fields under each User in the admin panel


# Remove django default user admin
admin.site.unregister(User)

# Register the user with our extra prfile fields
admin.site.register(User, Profile)