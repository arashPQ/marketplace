from django.db import models
from django.contrib.auth.models import User

from store.models import Product

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=256)
    shipping_email = models.EmailField()
    shipping_address1 = models.CharField(max_length=256)
    shipping_address2 = models.CharField(max_length=256, null=True, blank=True)
    shipping_city = models.CharField(max_length=256)
    shipping_state = models.CharField(max_length=256, null=True, blank=True)
    shipping_country = models.CharField(max_length=256, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Shipping Address"
    
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=256)
    email = models.EmailField()
    shipping_address = models.TextField(max_length=2500)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Order Items - {str(self.id)}'
