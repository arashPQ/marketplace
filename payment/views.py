from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import datetime

from cart.cart import Cart
from store.models import Product, UserProfile
from .forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItems

def payment_success(request):
    return render(request, 'payment/payment_success.html' ,{

    })

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantities
        total = cart.cart_total

        shipping_info = request.POST
        request.session['shipping_info'] = shipping_info            #   Create a session with shipping info


        if request.user.is_authenticated:             # If user logged in
            billing_form = PaymentForm()
            return render(request, "payment/billing.html", {
            'cart_products': cart_products,
            'quantities': quantities,
            'total': total,
            'shipping_info': shipping_info,
            'billing_form': billing_form
        })

        else:
            billing_form = PaymentForm()                                           # If user not logged in
            return render(request, "payment/billing.html", {
            'cart_products': cart_products,
            'quantities': quantities,
            'total': total,
            'shipping_info': request.POST,
            'billing_form': billing_form
        }) 
    
    else:
        messages.error(request, ("Oops!!... Access Denied !!"))
        return redirect('store:index')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    total = cart.cart_total
    

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {
        'cart_products': cart_products,
        'quantities': quantities,
        'total': total,
        'shipping_form': shipping_form
    })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {
        'cart_products': cart_products,
        'quantities': quantities,
        'total': total,
        'shipping_form': shipping_form
    })


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantities
        total = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        
        #   Get Shipping session data
        shipping_info = request.session.get('shipping_info')
        
        full_name = shipping_info['shipping_full_name']
        email = shipping_info['shipping_email']
        shipping_address = f"{shipping_info['shipping_address1']}\n{shipping_info['shipping_city']}\n{shipping_info['shipping_state']}\n{shipping_info['shipping_zipcode']}\n{shipping_info['shipping_country']}"
        amount_paid = total

        #       Create Order

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name,
                                email=email, shipping_address=shipping_address,
                                amount_paid=amount_paid )
            create_order.save()

            #   get order id && product info
            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id

                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItems(order_id=order_id, products_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
            
            #   Delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
        
            


            messages.success(request, ("Order Placed !"))
            return redirect('store:index')
    
        else:
            create_order = Order(full_name=full_name,
                                email=email, shipping_address=shipping_address,
                                amount_paid=amount_paid )
            create_order.save()

            #   get order id && product info
            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id

                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItems(order_id=order_id, products_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            #   Delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            
            current_user = UserProfile.objects.filter(user__id=request.user.id)
            #   Delete Shopping cart in database
            current_user.update(old_cart="")

            messages.success(request, ("Order Placed !"))
            return redirect('store:index')

    else:
        messages.error(request, ("Oops!!... Access Denied !!"))
        return redirect('store:index')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.get(id=pk)

        items = OrderItems.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipped_status']
            if status == 'true':
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
                messages.success(request, ("Shipping status updated!!"))
                return redirect('payment:shipped_dashboard')
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
                messages.success(request, ("Shipping status updated!!"))
                return redirect('payment:not_shipped_dashboard')


        return render(request, 'payment/order_detail.html', {
            "orders": orders,
            "items": items,
        })
    else:
        messages.error(request, ("Oops!!... Access Denied !!"))
        return redirect('store:index')


def not_shipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            status = request.POST['shipped_status']
            order_id = request.POST['order_id']
            order = Order.objects.filter(id=order_id)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
                
            messages.success(request, ("Shipping status updated!!"))
            return redirect('payment:shipped_dashboard')


        return render(request, "payment/not_shipped_dash.html", {
            "orders":orders,

        })
    

    else:
        messages.error(request, ("Oops!!... Access Denied !!"))
        return redirect('store:index')



def shipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        
        if request.POST:
            status = request.POST['shipped_status']
            order_id = request.POST['order_id']
            order = Order.objects.filter(id=order_id)
            order.update(shipped=False)     
            messages.success(request, ("Shipping status updated!!"))
            return redirect('payment:not_shipped_dashboard')

        return render(request, "payment/shipped_dash.html", {
            "orders":orders,

        })
    
    else:
        messages.error(request, ("Oops!!... Access Denied !!"))
        return redirect('store:index')
    

