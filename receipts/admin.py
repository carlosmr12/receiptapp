from django.contrib import admin
from .models import ExpenseCategory, Receipt, LineItem

admin.site.register(ExpenseCategory)
admin.site.register(Receipt)
admin.site.register(LineItem)
