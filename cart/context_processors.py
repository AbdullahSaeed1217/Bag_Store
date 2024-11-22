from .cart import Cart

def cart(request):
  # return the default data
  return { 'cart': Cart(request) }