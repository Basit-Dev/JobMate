# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'accounts'

# Define the url patterns
urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
]