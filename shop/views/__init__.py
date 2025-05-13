# shop/views/__init__.py
from .auth_views import user_login, user_logout, customer_signup
from .dashboard_views import *
from .product_views import *
from .cart_views import *
from .order_views import *
from .wishlist_views import *
from shop.views import general_views as views
from .general_views import home
from .product_views import add_product
from .cart_views import add_to_cart, cart_detail, remove_from_cart
from .order_views import order_detail
from .wishlist_views import wishlist_view, add_to_wishlist, remove_from_wishlist
