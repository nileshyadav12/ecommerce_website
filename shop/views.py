



# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import logout, authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth.models import Group

# from .models import Product, Order, Wishlist, Review, Cart, CartItem, Payment 
# from .forms import EditProfileForm, ProductForm, CustomerSignupForm, SellerSignupForm ,AddressForm
# from django.http import HttpResponse


# def home(request):
#     products_list = Product.objects.all()
#     paginator = Paginator(products_list, 10)  # Show 10 products per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     return render(request, 'shop/home.html', {'page_obj': page_obj})

# def customer_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.groups.filter(name='Sellers').exists():
#                 return redirect('seller_dashboard')
#             else:
#                 return redirect('customer_dashboard')
#         else:
#             messages.error(request, 'Invalid credentials. Please try again.')
#             return render(request, 'shop/customer_login.html')
    
#     return render(request, 'shop/customer_login.html')

# def seller_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.groups.filter(name='Sellers').exists():
#                 return redirect('seller_dashboard')
#             else:
#                 messages.error(request, 'Invalid credentials or not a seller account.')
#         else:
#             messages.error(request, 'Invalid credentials')

#     return render(request, 'shop/seller_login.html')

# def assign_user_to_group(user, group_name):
#     group, created = Group.objects.get_or_create(name=group_name)
#     user.groups.add(group)

# def customer_signup(request):
#     if request.method == 'POST':
#         form = CustomerSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             assign_user_to_group(user, 'Customers')
#             messages.success(request, 'Account created successfully! You are now logged in.')
#             return redirect('customer_dashboard')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = CustomerSignupForm()

#     return render(request, 'shop/signup_customer.html', {'form': form})

# def seller_signup(request):
#     if request.method == 'POST':
#         form = SellerSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             assign_user_to_group(user, 'Sellers')
#             messages.success(request, 'Account created successfully! You are now logged in.')
#             return redirect('seller_dashboard')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = SellerSignupForm()

#     return render(request, 'shop/signup_seller.html', {'form': form})

# @login_required
# def customer_dashboard(request):
#     orders = Order.objects.filter(customer=request.user)
#     return render(request, 'shop/customer_dashboard.html', {'orders': orders})

# @login_required
# def seller_dashboard(request):
#     products = Product.objects.filter(seller=request.user)
#     return render(request, 'shop/seller_dashboard.html', {'products': products})

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'shop/product_list.html', {'products': products})

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     reviews = Review.objects.filter(product=product)
#     return render(request, 'shop/product_detail.html', {'product': product, 'reviews': reviews})

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.seller = request.user  # Assign the logged-in user as the seller
#             product.save()
#             messages.success(request, 'Product added successfully!')
#             return redirect('add_product')
#         else:
#             messages.error(request, 'Error adding product. Please try again.')
#     else:
#         form = ProductForm()
    
#     return render(request, 'shop/add_product.html', {'form': form})

# @login_required
# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id, customer=request.user)
#     return render(request, 'order_detail.html', {'order': order})
# def checkout(request):
#     if request.method == "POST":
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             address = form.save(commit=False)
#             address.user = request.user  # assign user to the address
#             address.save()

#             # Continue with your order logic here...

#     else:
#         form = AddressForm()

#     return render(request, 'shop/checkout.html', {'form': form})





# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from .models import Product, Cart, CartItem
# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)  # Get the product or return 404 if not found
    
#     # Get or create the cart for the logged-in user, with `is_active=True`
#     cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

#     # Check if the product is already in the cart
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#     # If the item is already in the cart, increase the quantity
#     if not created:
#         cart_item.quantity += 1  # You can modify this if you want to use a custom quantity
#     cart_item.save()

#     return redirect('cart:cart_detail')  # Redirect to the cart detail page after adding


# from django.shortcuts import render
# from .models import Cart

# @login_required
# def cart_detail(request):
#     cart = Cart.objects.get(user=request.user, is_active=True)
#     cart_items = cart.cartitem_set.all()
#     total_price = sum(item.get_total_price() for item in cart_items)

#     return render(request, 'cart/cart_detail.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })


# @login_required
# def cart_view(request):
#     cart = Cart.objects.filter(user=request.user).first()
    
#     if cart:
#         items = cart.cartitem_set.all()  # Get all cart items for the cart
#         total_price = sum(item.get_total_price() for item in items)  # Calculate total price
#         return render(request, 'shop/cart_view.html', {'cart_items': items, 'total_price': total_price})
    
#     return render(request, 'shop/cart_empty.html')  # Render a template indicating the cart is empty

# @login_required
# def remove_from_cart(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
#     cart_item.delete()
#     return redirect('cart:cart_view')

# @login_required
# def cart_detail(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     return render(request, 'shop/cart_detail.html', {'cart': cart})

# def user_login(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     if created:
#         print(f"A new cart was created for {request.user.username}")
#     else:
#         print(f"Cart already exists for {request.user.username}")





# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from shop.models import Order, Product

# @login_required
# def dashboard(request):
#     """
#     Smart dashboard that redirects based on user type.
#     Shows order summary and quick actions like Flipkart-style dashboard.
#     """
#     user = request.user

#     if user.is_seller:
#         # Seller dashboard
#         products = Product.objects.filter(seller=user)
#         total_products = products.count()
#         return render(request, 'shop/seller_dashboard.html', {
#             'products': products,
#             'total_products': total_products
#         })

#     else:
#         # Customer dashboard
#         orders = Order.objects.filter(user=user).order_by('-created_at')
#         total_orders = orders.count()
#         return render(request, 'shop/customer_dashboard.html', {
#             'orders': orders,
#             'total_orders': total_orders
#         })
