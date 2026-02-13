
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from accounts.models import AdminUser , Customer
from orders.pdf import generate_invoice
from .models import Product
from django.contrib import messages
from orders.models import Order
from django.core.paginator import Paginator


from django.db.models import Sum


@login_required(login_url='/login/')
def admin_home(request):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')

    # ---------- POST: add product ----------
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        taxpercent = request.POST.get("taxpercent")
        stock = request.POST.get("stock")
        is_active = request.POST.get("is_active") == 'on'
        image = request.FILES.get("image")

        Product.objects.create(
            name=product_name,
            description=description,
            price=price,
            taxpercent=taxpercent,
            stock=stock,
            is_active=is_active,
            image=image
        )

        messages.success(request, "Product added successfully")
        return redirect('adminpanel:admin_home')

    # ---------- ALWAYS build dashboard data ----------
    all_products = Product.objects.all()
    orders = Order.objects.all()

    total_products = all_products.count()
    total_orders = orders.count()
    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_customers = Customer.objects.count()

    recent_orders = orders.order_by('-created_at')[:5]
    low_stock_products = all_products.filter(stock__lte=5)

    query = request.GET.get("q")
    if query:
        all_products = all_products.filter(name__icontains=query)
    paginator = Paginator(all_products, 5)  # 5 products per page
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    

    context = {
        'products': products,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }

    return render(request, 'adminpanel/adhome.html', context)
 


def delete_product(request, product_id):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully")
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist")
    
    return redirect('adminpanel:admin_home')
# Create your views here.

def update_product(request, product_id):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist")
        return redirect('adminpanel:admin_home')

    if request.method == "POST":
        product.name = request.POST.get("product_name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.taxpercent = request.POST.get("taxpercent")
        product.stock = request.POST.get("stock")
        product.is_active = request.POST.get("is_active") == 'on'
        
        if 'image' in request.FILES:
            product.image = request.FILES.get("image")

        product.save()
        messages.success(request, "Product updated successfully")
        return redirect('adminpanel:admin_home')

    context = {'product': product}
    return render(request, 'adminpanel/update_product.html', context)


def admin_orders(request):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    orders = Order.objects.all().order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'adminpanel/admin_orders.html', context)

def admin_order_detail(request, order_id):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    order = Order.objects.get(id=order_id)
    items = order.items.all()   

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.ORDER_STATUS_CHOICES):
            order.status = new_status
            order.save()
        return redirect("adminpanel:admin_order_detail", order_id=order.id)
    
    
    context = {'order': order, 'items': items,"status_choices": Order.ORDER_STATUS_CHOICES}
    return render(request, 'adminpanel/admin_order_detail.html', context)


def download_invoice(request, order_id):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    order = get_object_or_404(Order, order_id=order_id)
    return generate_invoice(order)
    # Logic to generate and return invoice PDF for the order