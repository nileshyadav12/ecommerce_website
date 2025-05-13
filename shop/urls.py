from django.contrib.auth import views as auth_views
from django.urls import path
# shop/urls.py
from shop.views.product_views import edit_product

from shop.views import (
    dashboard_views,
    profile_view,
    general_views,
    product_views,
    cart_views,
    order_views,
    checkout_views,
    wishlist_views,
    auth_views as custom_auth_views,
    order_views,
)

urlpatterns = [
    # -------------------------------
    # General Views
    # -------------------------------
    path('', general_views.home, name='home'),
    path('add_address/', checkout_views.add_address, name='add_address'),
    # -------------------------------
    # Authentication (User + Seller)
    # -------------------------------
    path('login/', custom_auth_views.user_login, name='login'),
    path('logout/', custom_auth_views.user_logout, name='logout'),
    path('customer/signup/', custom_auth_views.customer_signup, name='customer_signup'),
    path('seller/signup/', custom_auth_views.seller_signup, name='seller_signup'),
    path('customer/login/', custom_auth_views.user_login, {'user_type': 'customer'}, name='customer_login'),
    path('seller/login/', custom_auth_views.user_login, {'user_type': 'seller'}, name='seller_login'),
    path('order/<int:order_id>/invoice/', general_views.download_invoice, name='download_invoice'),
    path('order/<int:order_id>/invoice/', general_views.download_invoice, name='download_invoice'),
    
    
    
     path('customer/signup/', custom_auth_views.customer_signup, name='customer_signup'),
    
    # Login URL for customers
    path('customer/login/', custom_auth_views.user_login, {'user_type': 'customer'}, name='customer_login'),
    
    # Add customer dashboard path
    path('customer/dashboard/', custom_auth_views.customer_dashboard, name='customer_dashboard'), 
    # -------------------------------
    # Dashboards
    # -------------------------------
    path('customer/dashboard/', dashboard_views.customer_dashboard, name='customer_dashboard'),
    path('seller/dashboard/', dashboard_views.seller_dashboard, name='seller_dashboard'),

    # -------------------------------
    # Profile
    # -------------------------------
    path('profile/', profile_view, name='profile'),

    # -------------------------------
    # Product Management
    # -------------------------------
    path('products/', product_views.product_list, name='product_list'),
    path('products/my/', product_views.view_all_products, name='view_all_products'),
    path('product/<int:pk>/', product_views.product_detail, name='product_detail'),
    path('product/add/', product_views.add_product, name='add_product'),
    path('product/<int:product_id>/delete/', product_views.delete_product, name='delete_product'),
    path('product/<int:product_id>/manage-stock/', product_views.manage_stock, name='manage_stock'),
    path('product/<int:product_id>/buy/', cart_views.buy_now, name='buy_now'),

    # -------------------------------
    # Cart
    # -------------------------------
    path('cart/', cart_views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', cart_views.clear_cart, name='clear_cart'),

    # -------------------------------
    # Wishlist
    # -------------------------------
    path('wishlist/', wishlist_views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', wishlist_views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_item_id>/', wishlist_views.remove_from_wishlist, name='remove_from_wishlist'),

    # -------------------------------
    # Orders & Checkout
    # -------------------------------
    path('orders/', order_views.order_list, name='order_list'),
    path('order/<int:order_id>/', order_views.order_detail, name='order_detail'),
    path('order/confirmation/<int:order_id>/', order_views.order_confirmation, name='order_confirmation'),
    path('checkout/', order_views.checkout, name='checkout'),
    # Use product_views instead of views here
    path('product/edit/<int:pk>/', product_views.edit_product, name='edit_product'),
    
       path('wishlist/', wishlist_views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', wishlist_views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', wishlist_views.remove_from_wishlist, name='remove_from_wishlist'),
    path('update-status/<int:product_id>/', product_views.update_order_status, name='update_order_status'),
    
    path('notification/read/<int:notification_id>/', dashboard_views.mark_as_read, name='mark_as_read'),

]
