from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    daily_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()  # 🔥 very important

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField(auto_now_add=True)

    note = models.TextField(blank=True, null=True)  # optional

    def __str__(self):
        return f"{self.customer.name} - {self.amount}"