from django.contrib import admin
from .models import Category, Product, Customer, Order, UserProfile, SubCategory
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(UserProfile)
admin.site.register(SubCategory)

class ProfileInLine(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInLine]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
