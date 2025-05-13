from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Cart, CartItem, Order
from shop.forms import  ShippingDetailsForm

# -------------------------------
# Checkout View
# -------------------------------


from django.shortcuts import render
from shop.forms import AddressForm
from django.shortcuts import render, redirect
from shop.forms import AddressForm

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Ensure the address is associated with the logged-in user
            address = form.save(commit=False)
            address.user = request.user  # Assign the logged-in user to the address
            address.save()
            return redirect('checkout')  # Redirect after saving the address
    else:
        form = AddressForm()
    return render(request, 'shop/add_address.html', {'form': form})



# -------------------------------
# Another Checkout Implementation (with ShippingDetailsForm)
# -------------------------------

@login_required
def checkout_with_details(request):
    """
    Handle the checkout process with ShippingDetailsForm for custom shipping address.
    """
    # Get the user's cart items
    cart_items = CartItem.objects.filter(cart__user=request.user)
    
    # Calculate the total price of the cart
    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        # Handle form submission for shipping details
        form = ShippingDetailsForm(request.POST)
        if form.is_valid():
            # Create a new order with shipping details
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                shipping_address=form.cleaned_data['shipping_address'],
                status="Pending"  # Example order status
            )
            
            # Add the cart items to the order
            for item in cart_items:
                order.items.add(item.product)  # Assuming order has a related field for products
            
            # Clear the cart after the order is created (optional)
            cart_items.delete()

            # Set the flag to show the success message
            return render(request, 'shop/checkout.html', {
                'order_confirmed': True,
                'total_price': total_price,
                'cart': cart_items,  # Passing cart again in case there are any UI needs
                'form': form,
            })
    
    else:
        form = ShippingDetailsForm()  # If GET request, initialize an empty form

    # Render the checkout page
    return render(request, 'shop/checkout.html', {
        'total_price': total_price,
        'cart': cart_items,
        'form': form,
        'order_confirmed': False,  # Default to False until confirmed
    })


# -------------------------------
# Order Confirmation View
# -------------------------------

@login_required
def order_confirmation(request, order_id):
    """
    Display the order confirmation page once the order is successfully placed.
    """
    try:
        # Fetch the order details for the logged-in user
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Render the order confirmation page with the order details
        return render(request, 'shop/order_confirmation.html', {'order': order})
    
    except Order.DoesNotExist:
        # If the order does not exist, show an error message
        messages.error(request, "Order not found.")
        return redirect('shop/profile')  # Redirect the user back to the profile page
