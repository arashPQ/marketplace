from django.contrib import admin

from .models import ShippingAddress, Order, OrderItems

admin.site.register(ShippingAddress)
admin.site.register(OrderItems)

class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_order"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_order", "shipped", "date_shipped"]
    inlines = [OrderItemsInline]

admin.site.register(Order, OrderAdmin)