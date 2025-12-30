from django.contrib import admin
from .models import Transaction, TransactionLineItem

# Register your models here.

# Display transactions with inline items
class TransactionLineItemInline(admin.TabularInline):
    model = TransactionLineItem
    extra = 0


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "user",
        "job",
        "status",
        "subtotal",
        "service_fee",
        "total",
        "created_at",
    )
    inlines = [TransactionLineItemInline]