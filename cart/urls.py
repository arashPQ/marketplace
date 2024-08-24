from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/', views.add_cart, name='add'),
    path('update/', views.update_cart, name='update'),
    path('remove/', views.remove_cart, name='remove'),

    
]
