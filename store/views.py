from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from store.models import Product
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart



# Create your views here.


@login_required(login_url='Index')
def HomePage(request):
    products = Product.objects.all()
    cart = Cart(request)
    cart = request.session.get('cart', {})
    cart_items = cart  # Get cart dictionary from session
    cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart
    context = {
        'products': products,
        'cart_count': cart_count  # Pass the count to the template
    }
    
    return render(request, 'home.html', context)

def custom_login_redirect(request):
    return render(request, 'Error.html',{'data':"Login First!"})  # Custom page with message

   


@csrf_exempt
@login_required(login_url='Index')  # Use this only if necessary and if CSRF token is correctly handled in frontend
def add_to_cart(request):
    try:
        cart = Cart(request)
        cart = request.session.get('cart', {})
        cart_items = cart  # Get cart dictionary from session
        cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart
        # Get product ID and quantity, with default quantity as 1
        product_id = str(request.POST.get('product_id'))  # Convert to string for consistency in session
        quantity = int(request.POST.get('quantity', 1))

        # Initialize cart in session if it doesn't exist
        cart = request.session.get('cart', {})

        # Add or update the product in the cart
        if product_id in cart:
            cart[product_id] += quantity  # Update quantity if already in cart
        else:
            cart[product_id] = quantity  # Add new product

        # Save cart back to the session
        request.session['cart'] = cart
        request.session.modified = True  # Ensure session is saved
        cart = Cart(request)
        cart = request.session.get('cart', {})
        cart_items = cart  # Get cart dictionary from session
        cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart
        product = get_object_or_404(Product, id=product_id)
        # Return the updated cart count
        cart_count = sum(cart.values())  # Sum up the quantities of all items
        print(cart.values())  # Debugging line to show cart contents
        print(cart_count, "is cart count after add to cart")  # Debugging line to show cart count
        return render(request, 'view_product.html', {'product': product, 'cart_count': cart_count})

    except (ValueError, TypeError) as e:
        # Handle cases where `quantity` might not be convertible to int or `product_id` is invalid
        return JsonResponse({'message': 'Invalid product ID or quantity'}, status=400)
    
@login_required(login_url='Index')
def get_cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())  # Sum up the quantities of all items
    print("cart count is ",cart_count)
    return JsonResponse({'cart_count': cart_count})

@login_required(login_url='Index')
def view_cart(request):
    cart = Cart(request)
    cart = request.session.get('cart', {})
    cart_items = cart  # Get cart dictionary from session
    cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart

    cart = request.session.get('cart', {})
    print(cart.items())
    # return HttpResponse("cart")
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
            })
            total_price += product.retail_price * quantity
        except Product.DoesNotExist:
            continue  # Skip items if product doesn't exist

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart_count': cart_count})


@require_POST
@login_required(login_url='Index')
def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', {})

    if product_id in cart:
        del cart[product_id]  # Remove item from cart
        request.session['cart'] = cart
        request.session.modified = True

    return JsonResponse({'message': 'Product removed from cart', 'cart': cart})

@login_required(login_url='Index')
def view_product(request,product_id):
    cart = Cart(request)
    cart = request.session.get('cart', {})
    cart_items = cart  # Get cart dictionary from session
    cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'view_product.html', {'product': product, 'cart_count': cart_count})

@login_required(login_url='Index')
def AboutUs(request):
    cart = Cart(request)
    cart = request.session.get('cart', {})
    cart_items = cart  # Get cart dictionary from session
    cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart
    return render(request,'aboutUs.html',{'cart_count': cart_count})

@login_required(login_url='Index')
def Blog(request):
    cart = Cart(request)
    cart = request.session.get('cart', {})
    cart_items = cart  # Get cart dictionary from session
    cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart

    return render(request,'blog.html',{'cart_count':cart_count})

@login_required(login_url='Index')
def Contact(request):
    cart = Cart(request)
    cart = request.session.get('cart', {})
    cart_items = cart  # Get cart dictionary from session
    cart_count = sum(item['quantity'] for item in cart_items.values())  # Calculate total items in cart
    return render(request,'contactUs.html',{'cart_count':cart_count})