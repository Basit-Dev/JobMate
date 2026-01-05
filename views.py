from django.shortcuts import render


# This function will display the custom 404 page
def custom_404(request, exception):
    return render(request, "404.html")
