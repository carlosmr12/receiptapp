from django import forms
from django.contrib.auth.models import User
from .models import Receipt

class ReceiptUploadForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="User")

    class Meta:
        model = Receipt
        fields = ['image', 'category', 'user']