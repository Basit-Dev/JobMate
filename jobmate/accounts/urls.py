# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'accounts'

# Define the url patterns
urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('all_engineers/', views.all_engineers, name='all_engineers'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
]