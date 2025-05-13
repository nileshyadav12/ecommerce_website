# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib import messages
# from django.db import transaction
# from .models import Order, OrderItem, Product
# from django.contrib.auth.decorators import login_required
# from django.core.exceptions import ValidationError
# from .forms import OrderForm
# # -----------------------------
# def product_list(request):
#     """
#     Display a list of all products available in the store.
#     """
#     products = Product.objects.filter(available=True)  # Only show available products
#     return render(request, 'shop/product_list.html', {'products': products})
# # View to display all products
# def product_list(request):
#     products = Product.objects.all()  # Fetch all available products
#     return render(request, 'shop/product_list.html', {'products': products})

# # View to create an order
# @login_required
# def create_order(request):
#     if request.method == "POST":
#         try:
#             with transaction.atomic():
#                 # Create an order object
#                 order = Order.objects.create(
#                     user=request.user,
#                     total_price=request.POST.get('total_price'),
#                     payment_method=request.POST.get('payment_method'),
#                     status='pending',
#                     shipping_address=request.user.address,  # Assuming user has an address model
#                     phone=request.POST.get('phone'),
#                     email=request.user.email
#                 )

#                 # Process order items
#                 for item in request.POST.getlist('items'):
#                     product = Product.objects.get(id=item['product_id'])
#                     quantity = item['quantity']
#                     price = product.price
#                     # Create OrderItem objects
#                     OrderItem.objects.create(
#                         order=order,
#                         product=product,
#                         quantity=quantity,
#                         price=price,
#                         status='Pending'
#                     )
#                     # Update stock of the product
#                     product.update_stock(quantity)
#                 messages.success(request, "Your order has been placed successfully!")
#                 return redirect('order_detail', order_id=order.id)
#         except ValidationError as e:
#             messages.error(request, f"Error: {str(e)}")
#             return redirect('product_list')
#         except Exception as e:
#             messages.error(request, f"An error occurred: {str(e)}")
#             return redirect('product_list')

#     else:
#         return render(request, 'shop/create_order.html')


# # View to update order status (e.g., for sellers to mark as shipped or delivered)
# @login_required
# def update_order_status(request, order_item_id):
#     try:
#         order_item = OrderItem.objects.get(id=order_item_id)

#         if order_item.product.seller != request.user:
#             messages.error(request, "You are not authorized to update this order item.")
#             return redirect('order_detail', order_id=order_item.order.id)

#         if request.method == "POST":
#             new_status = request.POST.get('status')
#             order_item.status = new_status
#             order_item.save()

#             # If the item is shipped or delivered, update the product stock
#             order_item.update_stock_on_status_change()

#             messages.success(request, f"Order item status updated to {new_status}.")
#             return redirect('order_detail', order_id=order_item.order.id)

#     except OrderItem.DoesNotExist:
#         messages.error(request, "Order item not found.")
#         return redirect('product_list')

#     return render(request, 'shop/update_order_status.html', {'order_item': order_item})


# # View to display order details
# @login_required
# def order_detail(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id, user=request.user)
#         order_items = OrderItem.objects.filter(order=order)
#         return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})
#     except Order.DoesNotExist:
#         messages.error(request, "Order not found.")
#         return redirect('product_list')


# # API endpoint to get order status and update in real-time
# def order_status_update_api(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         order_items = OrderItem.objects.filter(order=order)
#         status_data = {
#             'order_id': order.id,
#             'status': order.status,
#             'order_items': [
#                 {'product_name': item.product.name, 'quantity': item.quantity, 'status': item.status}
#                 for item in order_items
#             ]
#         }
#         return JsonResponse(status_data, safe=False)
#     except Order.DoesNotExist:
#         return JsonResponse({"error": "Order not found."}, status=404)

# # View for seller notifications (optional, might be custom to your system)
# @login_required
# def seller_notifications(request):
#     # Get orders for the seller
#     products_sold = Product.objects.filter(seller=request.user)
#     orders = Order.objects.filter(order_items__product__in=products_sold).distinct()
#     return render(request, 'ahop/seller_notifications.html', {'orders': orders})
















from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from shop.models import Order, OrderItem, Product
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import OrderForm

# View to display all products (Only available products)
def product_list(request):
    """
    Display a list of all products available in the store.
    """
    products = Product.objects.filter(available=True)  # Only show available products
    return render(request, 'shop/product_list.html', {'products': products})

# View to create an order
@login_required
def create_order(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Create an order object
                order = Order.objects.create(
                    user=request.user,
                    total_price=request.POST.get('total_price'),
                    payment_method=request.POST.get('payment_method'),
                    status='pending',
                    shipping_address=request.user.address,  # Assuming user has an address model
                    phone=request.POST.get('phone'),
                    email=request.user.email
                )

                # Process order items
                for item in request.POST.getlist('items'):
                    product = Product.objects.get(id=item['product_id'])
                    quantity = item['quantity']
                    price = product.price
                    # Create OrderItem objects
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price,
                        status='Pending'
                    )
                    # Update stock of the product
                    product.update_stock(quantity)
                messages.success(request, "Your order has been placed successfully!")
                return redirect('order_detail', order_id=order.id)
        except ValidationError as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('product_list')

    else:
        return render(request, 'shop/create_order.html')


# View to update order status (e.g., for sellers to mark as shipped or delivered)
@login_required
def update_order_status(request, order_item_id):
    try:
        order_item = OrderItem.objects.get(id=order_item_id)

        if order_item.product.seller != request.user:
            messages.error(request, "You are not authorized to update this order item.")
            return redirect('order_detail', order_id=order_item.order.id)

        if request.method == "POST":
            new_status = request.POST.get('status')
            order_item.status = new_status
            order_item.save()

            # If the item is shipped or delivered, update the product stock
            order_item.update_stock_on_status_change()

            messages.success(request, f"Order item status updated to {new_status}.")
            return redirect('order_detail', order_id=order_item.order.id)

    except OrderItem.DoesNotExist:
        messages.error(request, "Order item not found.")
        return redirect('product_list')

    return render(request, 'shop/update_order_status.html', {'order_item': order_item})


# View to display order details
@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('product_list')


# API endpoint to get order status and update in real-time
def order_status_update_api(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        status_data = {
            'order_id': order.id,
            'status': order.status,
            'order_items': [
                {'product_name': item.product.name, 'quantity': item.quantity, 'status': item.status}
                for item in order_items
            ]
        }
        return JsonResponse(status_data, safe=False)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)

# View for seller notifications (optional, might be custom to your system)
@login_required
def seller_notifications(request):
    # Get orders for the seller
    products_sold = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(order_items__product__in=products_sold).distinct()
    return render(request, 'shop/seller_notifications.html', {'orders': orders})
