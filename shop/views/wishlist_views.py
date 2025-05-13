from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Wishlist, Product

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(customer=request.user)
    return render(request, 'shop/wishlist_view.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(customer=request.user, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(customer=request.user, product=product).delete()
    return redirect('wishlist')
