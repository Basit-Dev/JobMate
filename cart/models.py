from django.db import models
from django.db.models import Sum
import uuid
from django.conf import settings
from jobs.models import Job
from decimal import Decimal

# Create your models here.

# ADD ITEMS TO BASKET
class Transaction(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    # Unique transaction reference (safe for payments)
    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    # One order has many transactions
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    # Link each transaction to one job
    job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    # Totals for adjustments
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Stored Totals at checkout (Will be updated when payment processed)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    # # Total Adjustments calculator brain
    def recalculate_totals(self):
        """
        Single source of truth for ALL money fields
        """

        # Sum adjustment line items
        self.adjustment = (self.items.aggregate(total=Sum("line_total"))["total"]or Decimal("0.00"))

        # Base job cost
        base_cost = self.job.job_cost if self.job else Decimal("0.00")
        # Actual cost
        self.actual_cost = base_cost + self.adjustment

        # Totals derived from actual cost
        self.subtotal = self.actual_cost
        self.service_fee = self.subtotal * Decimal("0.15")
        self.vat = self.subtotal * Decimal("0.20")
        self.total = self.subtotal + self.vat - self.service_fee

        # Persist once
        self.save(update_fields=[
            "adjustment",
            "actual_cost",
            "subtotal",
            "service_fee",
            "vat",
            "total",
        ])

    def __str__(self):
        return f"Transaction {self.transaction_id} ({self.status})"


# ADD LINE ITEMS TO BASKET
class TransactionLineItem(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # Optional link to a job
    # job = models.ForeignKey(
    #     Job,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="transaction_line_items"
    # )

    description = models.CharField(
        max_length=255,
        help_text="e.g. Extra labour – 1.5 hours"
    )

    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Always calculate line total
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
