from django import forms
from django.contrib.auth.models import User
from .models import Receipt, LineItem

class ReceiptUploadForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="User")

    class Meta:
        model = Receipt
        fields = ['image', 'category', 'user']

class ReceiptEditForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['store', 'date_of_purchase', 'total_amount', 'category', 'user']
        widgets = {
            'date_of_purchase': forms.DateInput(attrs={'type': 'date'}),
        }

LineItemFormSet = forms.inlineformset_factory(Receipt, LineItem, fields=['description', 'price'], extra=1, can_delete=True)