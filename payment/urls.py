from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('success/', views.payment_success, name='success'),
    path('billing_info/', views.billing_info, name='billing'),
    path('checkout/', views.checkout, name='checkout')
]
