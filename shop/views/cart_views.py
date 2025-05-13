from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Cart, CartItem, Product

# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user, status='active')
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart_detail')


# Buy Now
@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    messages.success(request, f'Proceeding to checkout for {product.name}.')
    return redirect('checkout')


# Cart Detail
@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user, status='active').first()

    if cart:
        cart_items = cart.items.all()  # Using the correct related_name "items"
        total_price = sum(item.total_price for item in cart_items)  # total_price is a @property

        return render(request, 'shop/cart_detail.html', {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price
        })

    messages.error(request, "Your cart is empty.")
    return redirect('home')


# Remove from Cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('cart_detail')


# Clear Cart
@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user, status='active')
    cart.items.all().delete()  # Using the correct related_name "items"
    messages.success(request, "Your cart has been cleared.")
    return redirect('cart_detail')


# Update Cart Item Quantity
@login_required
def update_cart_quantity(request, cart_item_id):
    """
    Updates the quantity of an item in the cart.
    Expects POST data with 'quantity'.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == 'POST':
        try:
            new_qty = int(request.POST.get('quantity', 1))
            if new_qty < 1:
                messages.error(request, "Quantity must be at least 1.")
            else:
                cart_item.quantity = new_qty
                cart_item.save()
                messages.success(request, f"Updated quantity for {cart_item.product.name}.")
        except ValueError:
            messages.error(request, "Invalid quantity value.")
    return redirect('cart_detail')
