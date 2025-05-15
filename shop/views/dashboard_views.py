from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Order, Product, Notification, OrderItem
from django.core.mail import send_mail

# Seller Dashboard View
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
    notifications = Notification.objects.filter(
        product__seller=user, is_read=False).order_by('-created_at')

    return render(request, 'shop/seller_dashboard.html', {
        'products': products,
        'notifications': notifications
    })


# Customer Dashboard View
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


# Mark Notification as Read
@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('seller_dashboard')  # Redirect back to the dashboard


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


# Notify Seller When a Product is Purchased
def notify_seller(product, order):
    seller = product.seller
    send_mail(
        'Product Purchased!',
        f'Your product {product.name} has been purchased by {order.user.username}.',
        'admin@ecommerce.com',
        [seller.email],
        fail_silently=False,
    )


# Handle Order Purchase & Update Order Status
@login_required
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

    # Create a notification for the customer
    Notification.create_notification(
        recipient=request.user,
        message=f"Your order for '{product.name}' has been placed successfully!",
        product=product,
        order=order
    )

    # Create a notification for the seller
    Notification.create_notification(
        recipient=product.seller,
        message=f"Your product '{product.name}' has been purchased by {request.user.username}.",
        product=product,
        order=order
    )

    # Redirect or render a confirmation message to the customer
    messages.success(request, 'Your order has been placed successfully.')
    return redirect('customer_dashboard')


# View for Profile (common for customer/seller)
@login_required
def profile_view(request):
    """
    Display the profile of the logged-in user (customer or seller).
    """
    return render(request, 'shop/profile.html')  # Ensure the 'profile.html' template exists
