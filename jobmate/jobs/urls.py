# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'jobs'

# Define the url patterns
urlpatterns = [
    path('all_jobs/', views.all_jobs, name='all_jobs'),
    path('create_job/', views.create_job, name='create_job'),
    path('edit_job/', views.edit_job, name='edit_job'),
    path('job_detail/', views.job_detail, name='job_detail'),
]