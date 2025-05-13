from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Product, Order

# Home view - Show all products, regardless of who is logged in
# def home(request):
#     """
#     Display all products, with an optional search filter.
#     """
#     search_query = request.GET.get('search', '')
#     if search_query:
#         # If a search query exists, filter products by name
#         products = Product.objects.filter(name__icontains=search_query)
#     else:
#         # Otherwise, show all products
#         products = Product.objects.all()

#     return render(request, 'home.html', {'products': products})
def home(request):
    products = Product.objects.all()  # Fetch products from the database
    return render(request, 'home.html', {'products': products})

# Profile view - Fetch the orders for the logged-in user, ordered by the latest date
@login_required
def profile_view(request):
    """
    Display the user's orders on the profile page.
    """
    # Fetch orders for the logged-in user, ordered by the latest date
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')

    # Render the profile page with the user's orders
    return render(request, 'shop/profile.html', {'orders': orders})
# views.py
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from shop.models import Order
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from  shop.models import Order  # adjust path if needed

def download_invoice(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    template_path = 'shop/invoice_template.html'  # your template path
    context = {'order': order}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response.write(result.getvalue())
        return response
    return HttpResponse('Error while generating PDF', status=500)


