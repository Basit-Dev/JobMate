from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

# This function ensures that only admins can update, delete jobs
def admin_required(view_func):
    """
    Custom function to restrict access to Admin users only.
    Any non-admin user will be redirected.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get the currently logged-in user
        user = request.user

        # SAFETY CHECK:
        # 1. Make sure the user actually has a profile
        #    (prevents app from crashing if profile is missing)
        # 2. Check if the user's role is NOT admin
        #
        
        # Block anonymous users immediately
        if not user.is_authenticated:
            messages.error(request, "Please log in first.")
            return redirect("login")
        
        # If either condition is true → deny access
        if not hasattr(user, "profile") or user.profile.role != "Admin":
            # Show an error message to the user
            messages.error(
                request,
                "You do not have permission to access this page."
            )

            # Redirect the user to a safe page
            return redirect("jobs:all_jobs")

        # If the user is an admin:
        # Call the original view function and return its response
        return view_func(request, *args, **kwargs)

    # Return the wrapped version of the view
    return _wrapped_view