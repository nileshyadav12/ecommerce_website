# shop/views/ed_views.py

from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product
from shop.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

