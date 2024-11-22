class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add(self, product,productID):
        product_id = str(productID)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
        else:
            self.cart[product_id] = {
                'product_id': int(productID), 
                'title': product.title,
                'price': str(product.retail_price),
                'quantity': 1,
            }
        self.session['cart'] = self.cart
        self.session.modified = True

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session['cart'] = self.cart
            self.session.modified = True

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.session['cart'] = self.cart
            self.session.modified = True
