from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('success/', views.payment_success, name='success'),
    path('billing_info/', views.billing_info, name='billing'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order/', views.process_order, name="process_order"),
    path('shipped_dashboard/', views.shipped_dashboard, name='shipped_dashboard'),
    path('not_shipped_dashboard/', views.not_shipped_dashboard, name='not_shipped_dashboard'),
    path('order/<int:pk>/', views.orders, name='orders'),
    
]
