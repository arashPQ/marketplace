from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages


from .cart import Cart
from store.models import Product


def cart(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities

    totals = cart.cart_total()

    return render(request, 'cart/cart.html',{
        'cart_products': cart_products,
        'quantities': quantities,
        'totals':totals
    })



def add_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        product = get_object_or_404(Product, id=product_id)
        
        cart.add(product=product, quantity=product_quantity)

        cart_quantity = cart.__len__()

        # response = JsonResponse({
        #     'Product Name': product.name
        # })

        response = JsonResponse({
            'quantity': cart_quantity
        })
        messages.success(request, ("The product has been successfully added to the cart"))
        return response



def update_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        cart.update(product=product_id, quantity=product_quantity)

        response = JsonResponse({
            'quantity': product_quantity
            
            })
        messages.success(request, ("The product has been updated successfully"))
        return response



def remove_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        cart.delete(product=product_id)

        response = JsonResponse({
            'product': product_id
        })
        messages.warning(request, ("The product has been deleted successfully"))
        return response