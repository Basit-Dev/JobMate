# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'admin_dashboard'

# Define the url patterns
urlpatterns = [
    path('all_jobs/', views.all_jobs, name='all_jobs'),
    path('engineers/', views.engineers, name='engineers'),
    path('create_job/', views.create_job, name='create_job'),
    path('edit_job/', views.edit_job, name='edit_job'),
]