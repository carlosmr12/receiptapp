from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_receipt, name='upload_receipt'),
    path('list/', views.receipt_list, name='receipt_list'),
    path('<int:pk>/', views.receipt_detail, name='receipt_detail'),
    path('<int:pk>/edit/', views.edit_receipt, name='edit_receipt'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('chat/', views.chat_with_llm, name='chat_with_llm'),
]