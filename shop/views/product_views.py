from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product
from shop.forms import ProductForm

# -----------------------------
# Product List View
# -----------------------------
def product_list(request):
    """
    Display a list of all products available in the store.
    """
    products = Product.objects.filter(available=True)  # Only show available products
    return render(request, 'shop/product_list.html', {'products': products})


from django.shortcuts import render, get_object_or_404
from shop.models import Product, Notification
from django.contrib.auth.models import User

def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Add your order creation and purchase logic here
    
    # Create a notification for the seller
    notification_message = f"Your product '{product.name}' has been purchased!"
    notification = Notification(
        seller=product.seller,  # Assuming the seller is a ForeignKey in your Product model
        product=product,
        message=notification_message
    )
    notification.save()

    # Optionally, redirect to a confirmation page or back to the product page
    return render(request, 'shop/purchase_success.html', {'product': product})



# C:\Users\Deepak\api\ecommerce_website\shop\views\product_views.py
from django.shortcuts import redirect, get_object_or_404
from shop.models import Product  # or Order if you're updating order status
from django.contrib.auth.decorators import login_required

@login_required
def update_order_status(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        new_status = request.POST.get('order_status')
        if new_status:
            product.order_status = new_status
            product.save()
        return redirect('seller_dashboard')  # change to your actual dashboard name


# -----------------------------
# Product Detail View
# -----------------------------
def product_detail(request, pk):
    """
    Display detailed information about a specific product.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# -----------------------------
# Add Product View (Seller)
# -----------------------------
@login_required
def add_product(request):
    """
    Allow the logged-in seller to add a new product.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Set logged-in user as the seller
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('view_all_products')
        else:
            messages.error(request, 'Error adding product. Please check the form.')
    else:
        form = ProductForm()
    
    return render(request, 'shop/add_product.html', {'form': form})

# -----------------------------
# View All Seller's Products
# -----------------------------
@login_required
def view_all_products(request):
    """
    Show all products listed by the logged-in seller.
    """
    products = Product.objects.filter(seller=request.user)
    return render(request, 'shop/view_all_products.html', {'products': products})

# -----------------------------
# Delete Product View
# -----------------------------
@login_required
def delete_product(request, product_id):
    """
    Allow the logged-in seller to delete their own product.
    """
    product = get_object_or_404(Product, id=product_id)

    if product.seller == request.user:
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this product.')

    return redirect('view_all_products')

# -----------------------------
# Manage Stock View
# -----------------------------
@login_required
def manage_stock(request, product_id):
    """
    Allow the seller to update the stock quantity of a product.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        new_stock = request.POST.get('stock_quantity')

        if new_stock and new_stock.isdigit():
            product.quantity = int(new_stock)
            product.update_availability()
            product.save()
            messages.success(request, f'Stock for "{product.name}" updated successfully!')
        else:
            messages.error(request, 'Please enter a valid stock quantity.')

        return redirect('product_detail', pk=product.id)

    return render(request, 'shop/manage_stock.html', {'product': product})

# -----------------------------
# Buy Now View
# -----------------------------
@login_required
def buy_now(request, product_id):
    """
    Handle direct purchase of a product by redirecting to checkout.
    """
    product = get_object_or_404(Product, id=product_id)

    # You can enhance this by pre-filling checkout session with product info
    return redirect('checkout')  # Assuming there's a checkout view
# shop/views/product_views.py

from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product
from shop.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def edit_product(request, pk):
    """
    Edit an existing product. This view is accessible only by logged-in users.
    It allows updating a product's details.
    """
    # Fetch the product to edit using the primary key (pk)
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')  # Redirect to the product list or the edited product's page
        else:
            messages.error(request, 'Error updating product.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})
