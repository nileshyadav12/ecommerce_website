from django.urls import path
from django.contrib.auth import views as auth_views
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
    views_notifications
)

urlpatterns = [
    # -------------------------------
    # Notifications
    # -------------------------------
    path('notifications/', views_notifications.notification_list, name='notification_list'),
    path('notifications/read/<int:notification_id>/', views_notifications.mark_notification_as_read, name='mark_notification_as_read'),
    path('simulate/order/', views_notifications.simulate_order_purchase, name='simulate_order'),
    path('simulate/order/status/<int:order_id>/', views_notifications.simulate_seller_update_status, name='simulate_order_status'),
    path('notification/read/<int:notification_id>/', dashboard_views.mark_as_read, name='mark_as_read'),

    # -------------------------------
    # General
    # -------------------------------
    path('', general_views.home, name='home'),
    path('order/<int:order_id>/invoice/', general_views.download_invoice, name='download_invoice'),

    # -------------------------------
    # Authentication
    # -------------------------------
    path('login/', custom_auth_views.user_login, name='login'),
    path('logout/', custom_auth_views.user_logout, name='logout'),

    # Customer
    path('customer/signup/', custom_auth_views.customer_signup, name='customer_signup'),
    path('customer/login/', custom_auth_views.user_login, {'user_type': 'customer'}, name='customer_login'),
    path('customer/dashboard/', dashboard_views.customer_dashboard, name='customer_dashboard'),

    # Seller
    path('seller/signup/', custom_auth_views.seller_signup, name='seller_signup'),
    path('seller/login/', custom_auth_views.user_login, {'user_type': 'seller'}, name='seller_login'),
    path('seller/dashboard/', dashboard_views.seller_dashboard, name='seller_dashboard'),

    # -------------------------------
    # Profile
    # -------------------------------
    path('profile/', profile_view, name='profile'),

    # -------------------------------
    # Address / Checkout
    # -------------------------------
    path('add_address/', checkout_views.add_address, name='add_address'),
    path('checkout/', order_views.checkout, name='checkout'),

    # -------------------------------
    # Product Management
    # -------------------------------
    path('products/', product_views.product_list, name='product_list'),
    path('products/my/', product_views.view_all_products, name='view_all_products'),
    path('product/add/', product_views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', product_views.edit_product, name='edit_product'),
    path('product/<int:pk>/', product_views.product_detail, name='product_detail'),
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
    path('wishlist/remove/<int:product_id>/', wishlist_views.remove_from_wishlist, name='remove_from_wishlist'),

    # -------------------------------
    # Orders
    # -------------------------------
    path('orders/', order_views.order_list, name='order_list'),
    path('order/<int:order_id>/', order_views.order_detail, name='order_detail'),
    path('order/<int:order_id>/update_status/', order_views.update_order_status, name='update_order_status'),
    path('order/confirmation/<int:order_id>/', order_views.order_confirmation, name='order_confirmation'),
]
