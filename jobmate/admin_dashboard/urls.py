# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'admin_dashboard'

# Define the url patterns
urlpatterns = [
    path('all_jobs/', views.all_jobs, name='all_jobs'),
]