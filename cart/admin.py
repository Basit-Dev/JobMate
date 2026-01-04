from django.contrib import admin
from .models import Transaction, TransactionLineItem

# Register your models here.

# TRANSACTIONS
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
        "display_base_cost",
        "adjustment",
        "actual_cost",
        "status",
        "created_at",
    )

    readonly_fields = (
        "display_base_cost",
        "actual_cost",
        "created_at",
        "paid_at",
    )

    fields = (
        "order",
        "user",
        "job",
        "status",
        "display_base_cost",
        "adjustment",
        "actual_cost",
        "created_at",
        "paid_at",
    )

    inlines = [TransactionLineItemInline]

    def display_base_cost(self, obj):
        return obj.job.job_cost if obj.job else 0

    display_base_cost.short_description = "Base Cost"
