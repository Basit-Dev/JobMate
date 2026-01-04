from django.contrib import admin
from .models import Order, OrderItem
from cart.models import Transaction


# Register your models here.

# ORDERS
class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = (
        "job_base_cost",
        "adjustment",
        "actual_cost",
        "service_fee",
        "vat",
        "total",
    )
    fields = (
        "job",
        "job_base_cost",
        "adjustment",
        "actual_cost",
        "service_fee",
        "vat",
        "total",
        "status",
    )

    def job_base_cost(self, obj):
        return obj.job.job_cost if obj.job else "—"
    job_base_cost.short_description = "Base Cost"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "status", "created_at")
    readonly_fields = ("total", "stripe_session_id", "created_at")
    inlines = [TransactionInline]
