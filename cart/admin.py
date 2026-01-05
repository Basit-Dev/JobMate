from django.contrib import admin

# Import Transaction models
from .models import Transaction, TransactionLineItem

# TRANSACTION LINE ITEM INLINE
class TransactionLineItemInline(admin.TabularInline):
    """
    Displays individual adjustment line items
    inside a Transaction in the admin.
    """

    model = TransactionLineItem
    extra = 0  # Do not show empty extra rows


# TRANSACTION ADMIN
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Transaction records.

    A Transaction represents ONE completed job
    that may later be grouped into an Order.
    """

    # Columns shown in the Transaction list view
    list_display = (
        "transaction_id",       # UUID / reference ID
        "user",                 # Operative / user
        "job",                  # Related job
        "display_base_cost",    # Original job price
        "adjustment",           # Adjustment total
        "actual_cost",          # base_cost + adjustment
        "service_fee",          # Platform fee
        "vat",                  # VAT amount
        "total",                # Final charge
        "created_at",           # When transaction created
    )

    # Fields that must NOT be edited manually
    readonly_fields = (
        "display_base_cost",    # Computed from job
        "actual_cost",          # Calculated field
        "service_fee",          # Calculated field
        "vat",                  # Calculated field
        "total",                # Calculated field
        "created_at",           # Auto timestamp
    )

    # Order & limit fields shown on the Transaction edit page
    fields = (
        "order",                # Linked Order (after checkout)
        "user",                 # Owner of transaction
        "job",                  # Job reference
        "display_base_cost",    # Read-only base cost
        "adjustment",           # Editable adjustments
        "actual_cost",          # Calculated
        "created_at",
    )

    # Show adjustment line items inside the Transaction page
    inlines = [TransactionLineItemInline]


    # CUSTOM DISPLAY FIELD

    def display_base_cost(self, obj):
        """
        Returns the original job cost.
        This value is NOT stored on the Transaction model,
        but displayed for clarity in admin.
        """
        return obj.job.job_cost if obj.job else 0

    # Column label in admin
    display_base_cost.short_description = "Base Cost"
