from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
import json

from .models import Product, Category, UserProfile, SubCategory
from .forms import SignupForm, ConfigurationUser, ConfigurationPassword, UserInfoForm

from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress



def index(request):
    products = Product.objects.all()
    return render(request, "store/index.html",{
        'products': products
    })

def about(request):
    return render(request, "store/about.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = UserProfile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            #   convert database str to python dic
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("Welcome ..."))
            return redirect('store:index')
        else:
            messages.warning(request, ("Sorry !! something wrong ..."))
            return redirect('store:login')
    else:
        return render(request, 'store/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("See you later ..."))
    return redirect('store:index')

def register_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #   User loged in
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("User created . please fill out your information below..."))
            return redirect('store:info_configuration')
        else:
            messages.warning(request, ("Sorry !! something wrong ..."))
            return redirect('store:register')
    else:
        return render(request, 'store/register.html', {
            'form':form
        })
    

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/detail.html', {
        "product": product
    })

def category(request, cn):
    cn = cn.replace('-', ' ')

    try:
        category = Category.objects.get(name=cn)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {
            'products': products,
            'category': category
        })
    except:
        messages.warning(request, ("Sorry!! somethig wrong ..."))
        return redirect('store:index')



def subcategory(request, cn):
    sn = sn.replace('-', ' ')

    try:
        subcategory = SubCategory.objects.get(name=sn)
        products = Product.objects.filter(subcategory=subcategory)
        return render(request, 'store/category.html', {
            'products': products,
            'subcategory': subcategory
        })
    except:
        messages.warning(request, ("Sorry!! somethig wrong ..."))
        return redirect('store:index')





def user_configuration(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        configur_profile = ConfigurationUser(request.POST or None, instance=current_user)

        if configur_profile.is_valid():
            configur_profile.save()
            login(request, current_user)
            messages.success(request, ("Your Profile has been Updated"))
            return redirect('store:index')
        return render(request, "store/user_configuration.html", {
            'configur_profile':configur_profile,

        })
    else:
        messages.warning(request, ("You most be logged in to access your profile"))
        return redirect('store:index')


def info_configuration(request):
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)         # Get user shipping information
        
        configur_info = UserInfoForm(request.POST or None, instance=current_user)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user )

        if configur_info.is_valid() or shipping_form.is_valid():
            configur_info.save()
            shipping_form.save()

            messages.success(request, ("Your Profile Information has been Updated"))
            return redirect('store:index')
        return render(request, "store/info_configuration.html", {
            'configur_profile':configur_info,
            'shipping_form':shipping_form,

        })
    else:
        messages.warning(request, ("You most be logged in to access your profile"))
        return redirect('store:index')



def pass_configuration(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            password_form = ConfigurationPassword(current_user, request.POST)

            if password_form.is_valid():
                password_form.save()
                messages.success(request, ("Your Password has been Updated, Please Login again"))
                logout(request)
                return redirect('store:login')
            else:
                for error in list(password_form.errors.values()):
                    messages.error(request, error)
                    return redirect('password_configuration')
        else:
            password_form = ConfigurationPassword(current_user)
            return render(request, "store/password_configuration.html", {
                'password_form':password_form
            })
    else:
        messages.warning(request, ("You most be logged in to access your profile"))
        return redirect('store:index')
    

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.warning(request, ("Product not found"))
            return render(request, 'store/search.html', {})
        else:
            return render(request, 'store/search.html', {
                'searched':searched
            })
    else:    
        return render(request, 'store/search.html', {

    })