from django.contrib import admin
from .models import ExpenseCategory, Receipt

admin.site.register(ExpenseCategory)
admin.site.register(Receipt)
