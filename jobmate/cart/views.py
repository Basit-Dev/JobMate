from django.shortcuts import redirect, render,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Transaction
from cart.forms.adjustments import AdjustmentForm
from decimal import Decimal

# Create your views here.

@login_required
def payments(request):
    """
    This view renders the all payments page
    """
    return render(request, 'payments.html')


@login_required
def basket(request):
    """
    Basket grouped by user so each user paid separately
    """

    # Admin sees all open transactions, users see only theirs
    if request.user.profile.role == "Admin":
        transactions = Transaction.objects.filter(status="open")
    else:
        transactions = Transaction.objects.filter(user=request.user,status="open")

    # This will hold transactions by user
    user_basket = {}

    # Loop through each transaction and add correct transaction to correct user
    for job_transaction in transactions:
        user = job_transaction.user

        # Create the user basket with empty values
        if user not in user_basket:
            user_basket[user] = {
                "transactions": [],
                "subtotal": Decimal("0.00"),
                "service_fee": Decimal("0.00"),
                "vat": Decimal("0.00"),
                "total": Decimal("0.00"),
                "status": "open",
            }

        # Ensure actual_cost is always correct
        job_transaction.recalculate_totals()

        # Add transactions and subtotal to the correct users
        user_basket[user]["transactions"].append(job_transaction)
        user_basket[user]["subtotal"] += job_transaction.actual_cost

    # Loop through user basket items and calculate totals for service fee and total per user
    for user, data in user_basket.items():
        data["service_fee"] = data["subtotal"] * Decimal("0.15")  # 15%
        data["vat"] = data["subtotal"] * Decimal("0.20") # 20%
        data["total"] = data["subtotal"] + data["vat"] - data["service_fee"]

# Render the user basket
    return render(
        request,
        "basket.html",
        {
            "user_basket": user_basket
        }
    )


@login_required
def job_adjustment(request, transaction_id):
    """
    This view renders the job adjustment page
    """
    # Get pen transactions only
    open_transactions = Transaction.objects.filter(status="open")

    # Non-admin users can only access their own transactions, admin can view all transactions
    if request.user.profile.role != "Admin":
        open_transactions = open_transactions.filter(user=request.user)

    # Fetch the transaction or 404
    transaction = get_object_or_404(open_transactions, pk=transaction_id)

    # Form
    adjustment_form = AdjustmentForm()

    # If post request save the new data using the TransactionLineItem instance else GET the TransactionLineItem instance as a form with existing data
    if request.method == "POST":
        adjustment_form = AdjustmentForm(request.POST)
        if adjustment_form.is_valid():
            line_item = adjustment_form.save(commit=False)
            line_item.transaction = transaction
            line_item.save()
            transaction.recalculate_totals()
            messages.success(request, "Adjustment added!")
            return redirect("cart:job_adjustment", transaction_id=transaction.id)
    else:
        adjustment_form = AdjustmentForm()
    return render(request, 'job_adjustment.html', {"transaction": transaction, "adjustment_form": adjustment_form})
