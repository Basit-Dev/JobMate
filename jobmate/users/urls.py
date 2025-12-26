# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'users'

# Define the url patterns
urlpatterns = [
    path('logged_out/', views.logged_out, name='logged_out'),
    path('all_engineers/', views.all_engineers, name='all_engineers'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('profile_settings/<int:profile_id>/', views.profile_settings, name='profile_settings'),
]    