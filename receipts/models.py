from django.db import models

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Receipt(models.Model):
    image = models.ImageField(upload_to='receipt_images/')
    store = models.CharField(max_length=200, blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt from {self.store} on {self.date_of_purchase}"

class LineItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='line_items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} ({self.price})"
