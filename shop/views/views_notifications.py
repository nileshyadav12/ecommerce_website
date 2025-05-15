# views_notifications.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from shop.models import Notification, Product, Order, OrderItem


# ✅ View to list all notifications
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'shop/list.html', {'notifications': notifications})


# ✅ View to mark one notification as read
@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    return redirect('notification_list')


# ✅ Sample function to simulate a buyer placing an order
@login_required
def simulate_order_purchase(request):
    # Sample user and product (use your actual logic)
    buyer = request.user
    product = Product.objects.first()  # Replace with actual logic

    order = Order.objects.create(
        user=buyer,
        shipping_address=None,
        total_price=product.price,
        payment_method="cash_on_delivery"
    )

    OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)

    Notification.create_notification(
        recipient=product.seller,
        product=product,
        order=order,
        message=f"Your product '{product.name}' has been purchased by {buyer.username}."
    )

    return HttpResponse("Order simulated and notification sent to seller.")


# ✅ Sample function to simulate seller updating status
@login_required
def simulate_seller_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.update_status('shipped')  # This will call notify_users inside model

    return HttpResponse("Order status updated and notifications sent.")
