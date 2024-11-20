from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Wishlist, Order, OrderItem, Category, Customer
from .forms import ProductForm
from .forms import CategoryForm
from django.contrib import messages
from .forms import LoginForm
from django.http import HttpResponse


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')  # Redirect to the product list if already logged in

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('product_list')  # Redirect to a desired page after login
            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to a desired page after logout

def index(request):
    return render(request, 'index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    try:
        customer = request.user.customer  # Attempt to access the customer related to the user
    except Customer.DoesNotExist:
        messages.error(request, "You need to create a customer profile first.")
        return redirect('profile')  # Redirect the user to the profile page

    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': 1},
    )

    if not created:
        cart_item.quantity += 1  # If already in cart, just increase the quantity
        cart_item.save()

    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart')  # Redirect to cart page after adding

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer  # Accessing the related Customer object

    # Check if the product is already in the user's wishlist
    if Wishlist.objects.filter(customer=customer, product=product).exists():
        return HttpResponse("This product is already in your wishlist.", status=400)

    # Add product to wishlist
    Wishlist.objects.create(customer=customer, product=product)
    return redirect('wishlist')  # Redirect to the wishlist page

@login_required
def cart(request):
    customer = request.user.customer
    cart_items = Cart.objects.filter(customer=customer)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer  # Accessing the related Customer object

    # Get the cart item for the customer and product
    cart_item = Cart.objects.filter(customer=customer, product=product).first()

    if cart_item:
        cart_item.delete()
        return redirect('cart')  # Redirect to the cart page
    else:
        return HttpResponse("This product is not in your cart.", status=400)

@login_required
def wishlist(request):
    customer = request.user.customer
    wishlist_items = Wishlist.objects.filter(customer=customer)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer
    wishlist_item = Wishlist.objects.filter(customer=customer, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        return redirect('wishlist')  # Redirect to the wishlist page
    else:
        return HttpResponse("This product is not in your wishlist.", status=400)

@login_required
def checkout(request):
    # Checkout logic here
    return render(request, 'checkout.html')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('add_product')  # Redirect back to the product creation page
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or category list page
            return redirect('category_list')  # Assuming you have a category list view
    else:
        form = CategoryForm()

    return render(request, 'store/add_category.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

@login_required
def profile(request):
    # Check if the customer profile exists, if not create one
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle profile update here if needed
        pass

    return render(request, 'profile.html', {'customer': customer})