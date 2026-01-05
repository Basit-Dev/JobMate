# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'home'

# Define the url patterns
urlpatterns = [
    path('', views.home, name='home'),
]