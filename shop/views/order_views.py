# C:\Users\Deepak\api\ecommerce_website\shop\views\order_views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product, Cart, CartItem, Order
from shop.forms import CheckoutForm
# from shop.forms import ShippingForm
from shop.forms import CheckoutForm, ShippingDetailsForm
from shop.forms import CheckoutForm, ShippingDetailsForm


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
# Function to get the latest order status
# -------------------------------
def get_latest_order_status(product):
    latest_order = Order.objects.filter(product=product).order_by('-created_at').first()
    return latest_order.status if latest_order else "No orders yet"


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
#
from django.contrib import messages
from django.shortcuts import render, redirect
from  shop.forms import ShippingDetailsForm
from shop.models import Cart, Order

# @login_required
# def checkout(request):
#     """
#     Handle the checkout process by calculating the total price, processing the shipping
#     details, and creating an order based on the cart items of the logged-in user.
#     """
#     # Get the active cart for the logged-in user
#     cart = Cart.objects.filter(user=request.user, status='active').first()

#     # Ensure the cart exists and is not empty
#     if not cart or cart.items.count() == 0:
#         messages.error(request, "Your cart is empty. Please add products to your cart.")
#         return redirect('cart_detail')

#     # Calculate the total price of the cart
#     total_price = cart.calculate_total()

#     if request.method == 'POST':
#         form = ShippingDetailsForm(request.POST, user=request.user)
#         if form.is_valid():
#             # Create the order with shipping details
#             order = Order.objects.create(
#                 user=request.user,
#                 shipping_address=form.cleaned_data['shipping_address'],
#                 total_price=total_price,
#                 status="Pending"
#             )
            
#             # Add the cart items to the order
#             for cart_item in cart.items.all():
#                 order.order_items.create(
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     price=cart_item.product.price
#                 )
            
#             # Mark the cart as completed
#             cart.status = 'completed'
#             cart.save()

#             messages.success(request, "Your order has been successfully confirmed!")
#             return redirect('order_confirmation', order_id=order.id)
#     else:
#         form = ShippingDetailsForm(user=request.user)

#     return render(request, 'shop/checkout.html', {
#         'form': form,
#         'cart': cart,
#         'total_price': total_price,
#         'order_confirmed': False
#     })















# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from shop.models import Cart, Notification, Order
# from shop.forms import ShippingDetailsForm

# @login_required
# def checkout(request):
#     """
#     Handle the checkout process by calculating the total price, processing the shipping
#     details, and creating an order based on the cart items of the logged-in user.
#     """
#     cart = Cart.objects.filter(user=request.user, status='active').first()

#     if not cart or cart.items.count() == 0:
#         messages.error(request, "Your cart is empty. Please add products to your cart.")
#         return redirect('cart_detail')

#     total_price = cart.calculate_total()

#     if request.method == 'POST':
#         form = ShippingDetailsForm(request.POST, user=request.user)
#         if form.is_valid():
#             order = Order.objects.create(
#                 user=request.user,
#                 shipping_address=form.cleaned_data['shipping_address'],
#                 total_price=total_price,
#                 status="Pending"
#             )
            
#             for cart_item in cart.items.all():
#                 order.order_items.create(
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     price=cart_item.product.price
#                 )

#                 # ✅ Create notification for the seller
#                 Notification.objects.create(
#                     user=cart_item.product.seller,
#                     message=f"New order placed for your product '{cart_item.product.name}' by {request.user.username}."
#                 )

#             cart.status = 'completed'
#             cart.save()

#             messages.success(request, "Your order has been successfully confirmed!")
#             return redirect('order_confirmation', order_id=order.id)
#     else:
#         form = ShippingDetailsForm(user=request.user)

#     return render(request, 'shop/checkout.html', {
#         'form': form,
#         'cart': cart,
#         'total_price': total_price,
#         'order_confirmed': False
#     })

















from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Cart, Notification, Order
from shop.forms import ShippingDetailsForm

@login_required
def checkout(request):
    """
    Handle the checkout process by calculating the total price, processing the shipping
    details, and creating an order based on the cart items of the logged-in user.
    """
    cart = Cart.objects.filter(user=request.user, status='active').first()

    if not cart or cart.items.count() == 0:
        messages.error(request, "Your cart is empty. Please add products to your cart.")
        return redirect('cart_detail')

    total_price = cart.calculate_total()

    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST, user=request.user)
        if form.is_valid():
            # Create the order with shipping details
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                total_price=total_price,
                status="Processing"  # Change order status to 'Processing' or any other status
            )
            
            # Add the cart items to the order
            for cart_item in cart.items.all():
                order.order_items.create(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

                # ✅ Create notification for the seller
                Notification.objects.create(
                    seller=cart_item.product.seller,  # Make sure this is the seller field
                    product=cart_item.product,  # Ensure product is passed correctly
                    message=f"New order placed for your product '{cart_item.product.name}' by {request.user.username}."
                )

            # Mark the cart as completed
            cart.status = 'completed'
            cart.save()

            # Notify the user
            messages.success(request, "Your order has been successfully confirmed!")
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = ShippingDetailsForm(user=request.user)

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
        'order_confirmed': False
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
