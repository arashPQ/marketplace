from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('success/', views.payment_success, name='success'),
    path('error/', views.payment_error, name='error'),
    path('checkout/', views.checkout, name='checkout')
]
