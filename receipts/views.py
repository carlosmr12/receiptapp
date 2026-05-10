from django.shortcuts import render, redirect
from .forms import ReceiptUploadForm
from .llm_ocr import extract_receipt_data_with_openrouter
from .models import Receipt

def upload_receipt(request):
    if request.method == 'POST':
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save()

            # Perform OCR with LLM
            image_path = receipt.image.path
            extracted_data = extract_receipt_data_with_openrouter(image_path)

            if extracted_data:
                receipt.store = extracted_data.get('store')
                receipt.date_of_purchase = extracted_data.get('date_of_purchase')
                receipt.total_amount = extracted_data.get('total_amount')
                receipt.save()

            return redirect('receipt_list')  # Redirect to a list view after upload
    else:
        form = ReceiptUploadForm()
    return render(request, 'receipts/upload_receipt.html', {'form': form})

def receipt_list(request):
    receipts = Receipt.objects.all().order_by('-uploaded_at')
    return render(request, 'receipts/receipt_list.html', {'receipts': receipts})

def receipt_detail(request, pk):
    receipt = Receipt.objects.get(pk=pk)
    return render(request, 'receipts/receipt_detail.html', {'receipt': receipt})
