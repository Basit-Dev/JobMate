from django.contrib import admin
from django.db.models import Sum

from .models import Order
from cart.models import Transaction

# TRANSACTION INLINE (shown inside an Order)

class TransactionInline(admin.TabularInline):
    """
    Displays all Transactions that belong to an Order.
    Transactions are read-only because they are financial records.
    """

    model = Transaction
    extra = 0  # Do not show empty rows

    # Fields that can be viewed but NOT edited
    readonly_fields = (
        "job",                  # Job linked to this transaction
        "display_base_cost",    # Original job price, derived from Job
        "adjustment",           # Adjustment total
        "actual_cost",          # base_cost + adjustment
        "service_fee",          # Platform fee
        "vat",                  # VAT amount
        "total",                # Final transaction total
    )

    # Order & limit what appears in the table
    fields = (
        "job",
        "display_base_cost",
        "adjustment",
        "actual_cost",
        "service_fee",
        "vat",
        "total",
    )
    
    def display_base_cost(self, obj):
        """
        Base cost comes from the related Job, not Transaction.
        """
        if obj.job:
            return obj.job.job_cost
        return 0

    display_base_cost.short_description = "Base Cost"


# ORDER ADMIN

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin view for Orders.
    An Order represents ONE Stripe payment that may include
    multiple Transactions (jobs).
    """

    # Columns shown in Order list view
    list_display = (
        "id",
        "user",
        "subtotal_total",       # Sum of actual_costs
        "service_fee_total",    # Sum of service fees
        "vat_total",            # Sum of VAT
        "total",                # Stripe total
        "status",
        "created_at",
        "cancelled_at",
        "paid_at",

    )

    # Prevent manual editing of calculated financial values
    readonly_fields = (
        "subtotal_total",
        "service_fee_total",
        "vat_total",
        "total",
        "cancelled_at",
        "paid_at",
    )

    # Show related Transactions inside Order page
    inlines = [TransactionInline]

    # AGGREGATED ORDER TOTALS (calculated from Transactions)

    @admin.display(description="Subtotal (Order)")
    def subtotal_total(self, obj):
        """
        Sum of all transaction actual_cost values.
        This is the true subtotal before VAT & fees.
        """
        return obj.transactions.aggregate(
            total=Sum("actual_cost")
        )["total"] or 0

    @admin.display(description="Service Fee (Order)")
    def service_fee_total(self, obj):
        """
        Total service fee across all transactions.
        """
        return obj.transactions.aggregate(
            total=Sum("service_fee")
        )["total"] or 0

    @admin.display(description="VAT (Order)")
    def vat_total(self, obj):
        """
        Total VAT across all transactions.
        """
        return obj.transactions.aggregate(
            total=Sum("vat")
        )["total"] or 0
        
