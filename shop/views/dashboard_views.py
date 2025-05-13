# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from shop.models import Order, Product

# # View for displaying the profile of the logged-in user (customer or seller)
# @login_required
# def profile_view(request):
#     """
#     Display the profile of the logged-in user (customer or seller).
#     """
#     return render(request, 'shop/profile.html')  # Ensure the 'profile.html' template exists

# # View for the customer dashboard
# @login_required
# def customer_dashboard(request):
#     """
#     Display the dashboard for customers.
#     Shows their orders and order summary.
#     """
#     user = request.user
#     orders = Order.objects.filter(user=user).order_by('-created_at')  # Retrieve orders
#     total_orders = orders.count()  # Count total orders for display
#     return render(request, 'shop/customer_dashboard.html', {
#         'orders': orders,
#         'total_orders': total_orders,
#     })

# # View for the seller dashboard
# @login_required
# def seller_dashboard(request):
#     """
#     Display the dashboard for sellers.
#     Shows their products and product summary.
#     """
#     user = request.user
#     products = Product.objects.filter(seller=user)  # Retrieve products sold by the user
#     total_products = products.count()  # Count total products for display
#     return render(request, 'shop/seller_dashboard.html', {
#         'products': products,
#         'total_products': total_products,
#     })
# from django.shortcuts import render
# from shop.models import Product, Order
# def get_latest_order_status(product):
#     latest_order = Order.objects.filter(product=product).order_by('-created_at').first()
#     if latest_order:
#         return latest_order.status
#     return "No orders yet"
# def seller_dashboard(request):
#     products = Product.objects.filter(seller=request.user)
#     for product in products:
#         product.order_status = get_latest_order_status(product)
#     return render(request, 'seller_dashboard.html', {'products': products})
# # General Dashboard View (combined customer and seller logic)
# @login_required
# def dashboard_view(request):
#     """
#     Displays a unified dashboard based on whether the user is a customer or seller.
#     """
#     user = request.user
#     products = Product.objects.all()  # Get all products for public view
#     orders = Order.objects.filter(user=user)  # Get user orders
#     context = {
#         'products': products,
#         'orders': orders,
#         'user': user,
#         'is_customer': user.groups.filter(name='customer').exists(),  # Check if the user is a customer
#         'is_seller': user.groups.filter(name='seller').exists(),  # Check if the user is a seller
#     }
#     return render(request, 'shop/dashboard.html', context)




























from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Order, Product
from django.contrib import messages

# View for displaying the profile of the logged-in user (customer or seller)
@login_required
def profile_view(request):
    """
    Display the profile of the logged-in user (customer or seller).
    """
    return render(request, 'shop/profile.html')  # Ensure the 'profile.html' template exists

# View for the customer dashboard
@login_required
def customer_dashboard(request):
    """
    Display the dashboard for customers.
    Shows their orders and order summary.
    """
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')  # Retrieve orders
    total_orders = orders.count()  # Count total orders for display
    return render(request, 'shop/customer_dashboard.html', {
        'orders': orders,
        'total_orders': total_orders,
    })

# View for the seller dashboard
# @login_required
# def seller_dashboard(request):
#     """
#     Display the dashboard for sellers.
#     Shows their products and product summary.
#     """
#     user = request.user
#     products = Product.objects.filter(seller=user)  # Retrieve products sold by the user
#     total_products = products.count()  # Count total products for display

#     # Add order status to each product for display
#     for product in products:
#         product.order_status = get_latest_order_status(product)
#         product.delivery_status = get_delivery_status(product)

#     return render(request, 'shop/seller_dashboard.html', {
#         'products': products,
#         'total_products': total_products,
#     })




from django.shortcuts import render, get_object_or_404
from shop.models import Product, OrderItem

# View for Seller Dashboard
# @login_required
# def seller_dashboard(request):
#     """
#     Display the dashboard for sellers.
#     Shows products sold by the seller and their respective order statuses.
#     """
#     user = request.user
#     # Get all products sold by the seller
#     products = Product.objects.filter(seller=user)
    
#     for product in products:
#         # Get the latest order status for each product
#         order_items = OrderItem.objects.filter(product=product)
#         if order_items.exists():
#             # Get the latest status (by created_at date)
#             latest_order_item = order_items.order_by('-created_at').first()
#             product.latest_order_status = latest_order_item.status
#         else:
#             product.latest_order_status = "No orders yet"
    
#     return render(request, 'shop/seller_dashboard.html', {'products': products})


















from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shop.models import Product, OrderItem, Notification

@login_required
def seller_dashboard(request):
    """
    Display the dashboard for sellers.
    Shows products sold by the seller, their respective order statuses,
    and any unread notifications.
    """
    user = request.user

    # Get all products sold by the seller
    products = Product.objects.filter(seller=user)

    # Attach latest order status to each product
    for product in products:
        order_items = OrderItem.objects.filter(product=product)
        if order_items.exists():
            latest_order_item = order_items.order_by('-created_at').first()
            product.latest_order_status = latest_order_item.status
        else:
            product.latest_order_status = "No orders yet"

    # Get unread notifications
    notifications = Notification.objects.filter(seller=user, is_read=False).order_by('-created_at')

    return render(request, 'shop/seller_dashboard.html', {
        'products': products,
        'notifications': notifications
    })



from django.shortcuts import redirect

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('seller_dashboard')  # Redirect back to the dashboard






# Function to get the latest order status for a product
def get_latest_order_status(product):
    latest_order = Order.objects.filter(product=product).order_by('-created_at').first()
    if latest_order:
        return latest_order.status
    return "No orders yet"

# Function to get the delivery status of a product
def get_delivery_status(product):
    latest_order = Order.objects.filter(product=product).order_by('-created_at').first()
    if latest_order:
        return latest_order.delivery_status  # assuming the order has a 'delivery_status' field
    return "Not yet delivered"

# General Dashboard View (combined customer and seller logic)
@login_required
def dashboard_view(request):
    """
    Displays a unified dashboard based on whether the user is a customer or seller.
    """
    user = request.user
    products = Product.objects.all()  # Get all products for public view
    orders = Order.objects.filter(user=user)  # Get user orders
    context = {
        'products': products,
        'orders': orders,
        'user': user,
        'is_customer': user.groups.filter(name='customer').exists(),  # Check if the user is a customer
        'is_seller': user.groups.filter(name='seller').exists(),  # Check if the user is a seller
    }
    return render(request, 'shop/dashboard.html', context)

# Function to notify seller when a product is purchased
def notify_seller(product, order):
    seller = product.seller
    send_mail(
        'Product Purchased!',
        f'Your product {product.name} has been purchased by {order.user.username}.',
        'admin@ecommerce.com',
        [seller.email],
        fail_silently=False,
    )

# Function to update the delivery status of an order
def update_order_delivery_status(order, status):
    order.delivery_status = status
    order.save()

# Update Order Status and Notify Seller after Purchase
def handle_order_purchase(request, product_id):
    product = Product.objects.get(id=product_id)
    order = Order.objects.create(
        user=request.user,
        product=product,
        total_price=product.price,  # assuming the product has a price field
    )

    # Set initial order status
    order.status = 'pending'
    order.delivery_status = 'pending'  # Set initial delivery status as pending
    order.save()

    # Notify seller about the purchase
    notify_seller(product, order)

    # Redirect or render a confirmation message to the customer
    messages.success(request, 'Your order has been placed successfully.')
    return redirect('customer_dashboard')
