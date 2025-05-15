from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

from shop.models import Product, Order


# 🔹 Home View: Publicly accessible, shows all products
def home(request):
    """
    Display all products on the homepage, with optional search filter.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})


# 🔹 Profile View: Shows orders for the logged-in user
@login_required
def profile_view(request):
    """
    Display the logged-in user's order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'shop/profile.html', {'orders': orders})


# 🔹 PDF Invoice Download View
@login_required
def download_invoice(request, order_id):
    """
    Generate and download a PDF invoice for the specified order.
    """
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    template_path = 'shop/invoice_template.html'
    context = {'order': order}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

    if not pdf.err:
        response.write(result.getvalue())
        return response
    return HttpResponse('Error generating PDF invoice', status=500)
