# shop/views/ed_views.py

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
