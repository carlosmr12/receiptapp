from django.shortcuts import render, redirect
from .forms import ReceiptUploadForm
from .llm_ocr import extract_receipt_data_with_openrouter
from .models import Receipt, LineItem

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

                # Process line items
                line_items_data = extracted_data.get('line_items', [])
                for item_data in line_items_data:
                    LineItem.objects.create(
                        receipt=receipt,
                        description=item_data.get('description'),
                        price=item_data.get('price')
                    )

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
