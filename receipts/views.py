from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from .forms import ReceiptUploadForm
from .llm_ocr import extract_receipt_data_with_openrouter
from .models import Receipt, LineItem
from .reports import generate_expenses_by_category_pie, generate_spending_over_time_bar

def upload_receipt(request):
    if request.method == 'POST':
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user # Assign the current user
            receipt.save()
            form.save_m2m() # Save ManyToMany data for the form (e.g., categories)

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
    receipts = Receipt.objects.select_related('category', 'user').all().order_by('-uploaded_at')
    return render(request, 'receipts/receipt_list.html', {'receipts': receipts})

def receipt_detail(request, pk):
    receipt = Receipt.objects.get(pk=pk)
    return render(request, 'receipts/receipt_detail.html', {'receipt': receipt})

@login_required
def dashboard_view(request):
    # Get all users for filtering (only if superuser)
    all_users = User.objects.all()
    selected_user_ids = request.GET.getlist('users')
    period = request.GET.get('period', 'all_time')

    # Start with all receipts
    receipts_queryset = Receipt.objects.all()

    # Filter by user(s)
    if not request.user.is_superuser:
        # Non-superusers can only see their own receipts
        receipts_queryset = receipts_queryset.filter(user=request.user)
        selected_user_ids = [str(request.user.id)] # Ensure their own ID is selected
    elif selected_user_ids and 'all' not in selected_user_ids:
        # Superuser can filter by selected users
        receipts_queryset = receipts_queryset.filter(user__id__in=selected_user_ids)
    # If 'all' is selected or no users are selected by superuser, show all receipts

    # Filter by date period
    today = datetime.now().date()
    if period == 'last_7_days':
        start_date = today - timedelta(days=7)
        receipts_queryset = receipts_queryset.filter(date_of_purchase__gte=start_date)
    elif period == 'last_30_days':
        start_date = today - timedelta(days=30)
        receipts_queryset = receipts_queryset.filter(date_of_purchase__gte=start_date)
    elif period == 'this_month':
        start_date = today.replace(day=1)
        receipts_queryset = receipts_queryset.filter(date_of_purchase__gte=start_date)
    elif period == 'this_year':
        start_date = today.replace(month=1, day=1)
        receipts_queryset = receipts_queryset.filter(date_of_purchase__gte=start_date)

    # Generate plots
    pie_chart_html = generate_expenses_by_category_pie(receipts_queryset)
    bar_chart_html = generate_spending_over_time_bar(receipts_queryset, period=period)

    context = {
        'pie_chart': pie_chart_html,
        'bar_chart': bar_chart_html,
        'all_users': all_users if request.user.is_superuser else [],
        'selected_user_ids': [int(uid) for uid in selected_user_ids if uid != 'all'],
        'selected_period': period,
    }
    return render(request, 'receipts/dashboard.html', context)
