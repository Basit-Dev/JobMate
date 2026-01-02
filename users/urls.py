# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'users'

# Define the url patterns
urlpatterns = [
    path('logged_out/', views.logged_out, name='logged_out'),
    path('all_operatives/', views.all_operatives, name='all_operatives'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('profile_settings/<int:profile_id>/', views.profile_settings, name='profile_settings'),
    path('delete_operative/<int:profile_id>/', views.delete_operative, name='delete_operative'),
]    