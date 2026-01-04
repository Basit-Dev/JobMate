from django.shortcuts import redirect, render,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Transaction, TransactionLineItem
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
    
    # Get the current user
    user = request.user

    # Admin sees all open transactions, users see only theirs
    if request.user.profile.role == "Admin":
        transactions = Transaction.objects.filter(status="open")
    else:
        transactions = Transaction.objects.filter(
            user=request.user, status="open")
        
    # If delete btn is pressed delete the line and recalculate totals
    if request.method == "POST" and "delete_btn" in request.POST:

        # Get the id from the input field when delete btn pressed
        transaction_id = request.POST.get("basket_item_id")
            
        # Save the basket_item_id in Transaction.id so we know which line item to delete, keep the delete item related to this transaction only
        transaction = get_object_or_404(
            Transaction,
            id=transaction_id,
            status="open",
        )
        # Delete items permission check
        if user.profile.role != "Admin" and transaction.user != user:
            messages.error(request, "You do not have permission to delete this item.")
            return redirect("jobs:all_jobs")
        
        # Update the job status only if the job exists to in progress and save then delete transaction from basket
        if transaction.job:
            transaction.job.status = "in_progress"
            transaction.job.save(update_fields=["status"])
            
        # Delete the transaction from basket
        transaction.delete()
        # Display message
        messages.success(request, "Job removed from the basket!")
        return redirect("cart:basket")  

    # RUN BASKET DISPLAY
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
        
        # Add transactions and subtotal to the correct users inuser_basket
        user_basket[user]["transactions"].append(job_transaction)
        
        # From the job_transaction add the totals to user_basket items
        user_basket[user]["subtotal"] += job_transaction.subtotal
        user_basket[user]["service_fee"] += job_transaction.service_fee
        user_basket[user]["vat"] += job_transaction.vat
        user_basket[user]["total"] += job_transaction.total
    
# Render the user basket
    return render(
        request,
        "basket.html",
        {
            "user_basket": user_basket,
        }
    )


@login_required
def job_adjustment(request, transaction_id):
    """
    This view renders the job adjustment page
    """

    # Get the current user
    user = request.user

    # Fetch the transaction model or 404
    transaction = get_object_or_404(
        Transaction,
        pk=transaction_id,
        status="open"
    )

    # Page permission check
    if user.profile.role != "Admin" and transaction.user != user:
        messages.error(
            request, "You do not have permission to access this job.")
        return redirect("jobs:all_jobs")

    # Form
    adjustment_form = AdjustmentForm()

    # If post request save the new data using the TransactionLineItem instance else GET the TransactionLineItem instance as a form with existing data
    if request.method == "POST" and "add_adjustment" in request.POST:
        adjustment_form = AdjustmentForm(request.POST)

        # Add line items permission check
        if user.profile.role != "Admin" and transaction.user != user:
            messages.error(
                request, "You do not have permission to add this item.")
            return redirect("jobs:all_jobs")
        
        # Save item if form is valid
        if adjustment_form.is_valid():
            line_item = adjustment_form.save(commit=False)
            line_item.transaction = transaction
            line_item.save()
            transaction.recalculate_totals()
            messages.success(request, "Adjustment dded!")
            return redirect("cart:job_adjustment", transaction_id=transaction.id)
        
    # If delete btn is pressed delete the line and recalculate totals
    elif request.method == "POST" and "delete_btn" in request.POST:

        # Get the id from the input field when delete btn pressed
        line_item_id = request.POST.get("line_item_id")

        # Delete items permission check
        if user.profile.role != "Admin" and transaction.user != user:
            messages.error(
                request, "You do not have permission to delete this item.")
            return redirect("jobs:all_jobs")
        # Save the line_item_id in TransactionLineItem.id so we know which line item to delte, keep the delete item related to this transaction only
        item = get_object_or_404(
            TransactionLineItem,
            id=line_item_id,
            transaction=transaction
        )
        # Delete line ie: item = 15, so delete item 15, recalculate totals, send message, redirect
        item.delete()
        transaction.recalculate_totals()
        messages.success(request, "Adjustment deleted!")
        return redirect("cart:job_adjustment", transaction_id=transaction.id)
    else:
        # If NOT posting or getting data then load the value from the instance
        adjustment_form = AdjustmentForm()
    # Render page and context
    return render(request, 'job_adjustment.html', {"transaction": transaction, "adjustment_form": adjustment_form})
