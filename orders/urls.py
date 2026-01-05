# We are going to define the specific url for home app
#  import path

from django.urls import path
from . import views

app_name = 'orders'

# Define the url patterns
urlpatterns = [
    path('create_order_from_cart/<int:user_id>', views.create_order_from_cart, name='create_order_from_cart'),
    path("checkout/<int:order_id>/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.payment_success, name="payment_success"),
    path("cancel/<int:order_id>/", views.payment_cancel, name="payment_cancel"),
]