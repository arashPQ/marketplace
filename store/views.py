from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q

from .models import Product, Category, UserProfile
from .forms import SignupForm, ConfigurationUser, ConfigurationPassword, UserInfoForm

def index(request):
    products = Product.objects.all()
    return render(request, "index.html",{
        'products': products
    })

def about(request):
    return render(request, "about.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome ..."))
            return redirect('index')
        else:
            messages.warning(request, ("Sorry !! something wrong ..."))
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("See you later ..."))
    return redirect('index')

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
            return redirect('info_configuration')
        else:
            messages.warning(request, ("Sorry !! something wrong ..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {
            'form':form
        })
    

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'detail.html', {
        "product": product
    })

def category(request, cn):
    cn = cn.replace('-', ' ')

    try:
        category = Category.objects.get(name=cn)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {
            'products': products,
            'category': category
        })
    except:
        messages.warning(request, ("Sorry!! somethig wrong ..."))
        return redirect('index')


def user_configuration(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        configur_profile = ConfigurationUser(request.POST or None, instance=current_user)

        if configur_profile.is_valid():
            configur_profile.save()
            login(request, current_user)
            messages.success(request, ("Your Profile has been Updated"))
            return redirect('index')
        return render(request, "user_configuration.html", {
            'configur_profile':configur_profile,

        })
    else:
        messages.warning(request, ("You most be logged in to access your profile"))
        return redirect('index')


def info_configuration(request):
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        configur_info = UserInfoForm(request.POST or None, instance=current_user)

        if configur_info.is_valid():
            configur_info.save()

            messages.success(request, ("Your Profile Information has been Updated"))
            return redirect('index')
        return render(request, "info_configuration.html", {
            'configur_profile':configur_info,

        })
    else:
        messages.warning(request, ("You most be logged in to access your profile"))
        return redirect('index')



def pass_configuration(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            password_form = ConfigurationPassword(current_user, request.POST)

            if password_form.is_valid():
                password_form.save()
                messages.success(request, ("Your Password has been Updated, Please Login again"))
                logout(request)
                return redirect('login')
            else:
                for error in list(password_form.errors.values()):
                    messages.error(request, error)
                    return redirect('password_configuration')
        else:
            password_form = ConfigurationPassword(current_user)
            return render(request, "password_configuration.html", {
                'password_form':password_form
            })
    else:
        messages.warning(request, ("You most be logged in to access your profile"))
        return redirect('index')
    

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.warning(request, ("Product not found"))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {
                'searched':searched
            })
    else:    
        return render(request, 'search.html', {

    })