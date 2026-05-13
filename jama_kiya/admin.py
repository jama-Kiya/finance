from django.contrib import admin
from .models import Customer,Payment,User


@admin.register(Payment)
class Paymentadmin(admin.ModelAdmin):
    list_display=("amount","received_by","date","note")

@admin.register(Customer)
class Customeradmin(admin.ModelAdmin):
    list_display=("name","phone","address","daily_amount","start_date")