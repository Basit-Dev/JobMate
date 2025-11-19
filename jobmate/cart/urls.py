# We are going to define the specific url for home app
#  import path 

from django.urls import path
from . import views

app_name = 'cart'

# Define the url patterns
urlpatterns = [
    path('payments/', views.payments, name='payments'),
    path('basket/', views.basket, name='basket'),
]