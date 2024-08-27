from store.models import Product, UserProfile

class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request


        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {
            #     'price': str(product.price)
            # }
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)
            #   Convert Dictionary to Json      {'1':1} -> {"1":1}
            Jcart = str(self.cart)
            Jcart = Jcart.replace("\'", "\"")
            current_user.update(old_cart=str(Jcart))

    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quantities(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = int(quantity)
        
        # Get cart
        ourcart = self.cart

        # Update cart
        ourcart[product_id] = product_quantity

        self.session.modified = True
        carts = self.cart

        #   Save updated cart when logout and login again

        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)
            #   Convert Dictionary to Json      {'1':1} -> {"1":1}
            Jcart = str(self.cart)
            Jcart = Jcart.replace("\'", "\"")
            current_user.update(old_cart=str(Jcart))

        return carts

    def delete(self, product):
        product_id = str(product)

        # Delete from cart
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True

        #   Save deleted cart when logout and login again

        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)
            #   Convert Dictionary to Json      {'1':1} -> {"1":1}
            Jcart = str(self.cart)
            Jcart = Jcart.replace("\'", "\"")
            current_user.update(old_cart=str(Jcart))


    def cart_total(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            key = int(key)          #   convert to integer for math

            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)
            #   Convert Dictionary to Json      {'1':1} -> {"1":1}
            Jcart = str(self.cart)
            Jcart = Jcart.replace("\'", "\"")
            current_user.update(old_cart=str(Jcart))


