from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=11, blank=True)
    address1 = models.CharField(max_length=128, blank=True)
    address2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)           # postal code
    country = models.CharField(max_length=128, blank=True)
    old_cart = models.CharField(max_length=256, blank=True, null=True)


    def __str__(self):
        return self.user.username
    

    def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = UserProfile(user=instance)
            user_profile.save()

    post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'



class SubCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'SubCategories'


class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=256, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product-image/')      # media/uploads/product-image

    #   Add Sale items

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)


    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=128, default='', blank=True)
    phone = models.CharField(max_length=11, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.product