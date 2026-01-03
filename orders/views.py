
from django.shortcuts import get_object_or_404, redirect, render
from decimal import Decimal
from cart.models import Transaction
from .models import Order
import stripe
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from .models import Order
from helpers.permission_check import admin_required
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

# CREATE A ORDER FRIOM BASKET
@login_required
@admin_required
def create_order_from_cart(request, user_id):
    """
    Create an Order from ALL open Transactions for the user
    """

    # Get the filtered values from the user id that was sent from checkout button in basket page also get only open transactions
    transactions = Transaction.objects.filter(
        user=user_id,
        status="open", 
    )

    # If there are no transactions return to basket
    if not transactions.exists():
        messages.error(request, "There are no trasactions to display!")
        return redirect("cart:basket")

    # Create one Order object with the values of the given user_id, status is pending and total = 0.00
    order = Order.objects.create(
        user_id=user_id,
        status=Order.Status.PENDING,
        total=Decimal("0.00"),
    )

    # Will use to save the calculated total at line 47
    total = Decimal("0.00")

# Loop through tasactions and get totals
    for totals in transactions:
        subtotal = totals.subtotal
        service_fee = subtotal * Decimal("0.15")
        vat = subtotal * Decimal("0.20")
        total = subtotal + vat - service_fee
    
    # Save total in Order object   
    order.total = total
    order.save(update_fields=["total"])
    print("TOTAL", order.total)

    # The Stripe checkout function will run once the browser hits "GET /orders/checkout/99/ 
    return redirect("orders:checkout", order_id=order.id)


# STRIPE CHECKOUT FUNCTION
@admin_required
@login_required
def checkout(request, order_id):
    # Get the order id from  create_order_from_cart
    order = get_object_or_404(Order, id=order_id)

    # Create a stripe session
    checkout_session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    mode="payment",
    
    # Stripe checkout order
    line_items=[
        {
            "price_data": {
                "currency": "gbp",
                "unit_amount": int(order.total * 100),
                "product_data": {
                    "name": f"Payment for { order.user.get_full_name() }",
                },
            },
            "quantity": 1,
        }
    ],
    # Where Stripe sends the user if success or cancel
    success_url=settings.SITE_URL + reverse("orders:payment_success", kwargs={"order_id": order.id}),
    cancel_url=settings.SITE_URL + reverse("orders:payment_cancel", kwargs={"order_id": order.id}),
)

    # Store Stripe session ID
    order.stripe_session_id = checkout_session.id
    order.save(update_fields=["stripe_session_id"])
    return redirect(checkout_session.url)


# SUCCESS PAYMENT FUNCTION RENDERS SUCCESS PAGE
@admin_required
@login_required
def payment_success(request, order_id):
    
    # Get the Order object with the order_id stripe holds that came from the cart    
    order = get_object_or_404(Order, id=order_id)

    # If status is not equal to paid then order status = paid and save the status in object
    if order.status != Order.Status.PAID:
        order.status = Order.Status.PAID
        order.save(update_fields=["status"])
        
    # Mark related transactions as paid in the Transaction model
    Transaction.objects.filter(
        user_id=order.user_id,
        status="open",).update(status="paid")

    # Render the success page
    return render(request, "payment_success.html", {"order": order})


# CANCEL PAYMENT FUNCTION DRENDERS CANCEL PAGE
@admin_required
@login_required
def payment_cancel(request, order_id):
    
    # Get the Order object with the order_id stripe holds that came from the cart    
    order = get_object_or_404(Order, id=order_id)

    # If status is equal to pending then order status = cancelled and save the status in object
    if order.status == Order.Status.PENDING:
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status"])

    # Render the cancel page
    return render(request, "payment_cancel.html", {"order": order})
