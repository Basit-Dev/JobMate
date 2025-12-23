from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not hasattr(user, "profile") or user.profile.role != "admin":
            messages.error(request, "You do not have permission to access this page.")
            return redirect("jobs:all_jobs")

        return view_func(request, *args, **kwargs)

    return _wrapped_view