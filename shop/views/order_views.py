from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product, Cart, CartItem, Order, Notification
from shop.forms import ShippingDetailsForm

# -------------------------------
# View for Order List
# -------------------------------
@login_required
def order_list(request):
    # Get orders for the logged-in user, ordered by most recent
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    if not orders:
        messages.info(request, "You have no orders yet.")
    return render(request, 'shop/order_list.html', {'orders': orders})

# -------------------------------
# View for Order Detail
# -------------------------------
@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('order_list')
    return render(request, 'shop/order_detail.html', {'order': order})

# -------------------------------
# Checkout View
# -------------------------------

# Checkout Logic
@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user, status='active').first()

    if not cart or cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    total_price = cart.calculate_total()

    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST, user=request.user)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                total_price=total_price,
                status="Processing"
            )

            for cart_item in cart.items.all():
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    status='Pending'
                )

                Notification.objects.create(
                    recipient=cart_item.product.seller,
                    product=cart_item.product,
                    message=f"New order for '{cart_item.product.name}' by {request.user.username}."
                )

            Notification.objects.create(
                recipient=request.user,
                message="Your order has been placed successfully."
            )

            cart.status = 'completed'
            cart.save()

            messages.success(request, "Order placed successfully.")
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = ShippingDetailsForm(user=request.user)

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
    })
# -------------------------------
# Order Confirmation View
# -------------------------------
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_confirmation.html', {'order': order})


# -------------------------------
# Optional: Confirm Order (Legacy)
# -------------------------------
@login_required
def confirm_order(request):
    if request.method == "POST":
        new_order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            total_price=100798.00,  # This should ideally come from the cart
            payment_method=request.POST.get('payment_method'),
            status='pending',
        )
        messages.success(request, "Order has been successfully placed!")
        return redirect('shop/profile')  # Or your user dashboard/profile view
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from shop.models import Product
from shop.models import Product, Cart, CartItem, Order, Notification, OrderItem
@login_required
def update_order_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        new_status = request.POST.get('order_status')
        if new_status:
            order_items = OrderItem.objects.filter(product=product)
            for item in order_items:
                item.status = new_status
                item.save()

                item.order.status = new_status
                item.order.save()

                Notification.objects.create(
                    recipient=item.order.user,
                    product=product,
                    message=f"The status of your order for '{product.name}' is now '{new_status}'."
                )

            product.order_status = new_status
            product.save()
            print(f"Updated '{product.name}' to '{new_status}'")

        return redirect('seller_dashboard')

