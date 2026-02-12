
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from accounts.models import AdminUser
from orders.pdf import generate_invoice
from .models import Product
from django.contrib import messages
from orders.models import Order

@login_required(login_url='/login/')
def admin_home(request):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login') 
    
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
    return render(request, 'adminpanel/adhome.html')
@login_required(login_url='/login/')
def adminpd(request):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    q=Product.objects.all()

    
    if request.GET.get('q'):
        q=q.filter(name__icontains=request.GET.get('q'))


    context={'products':q}
    return render(request, 'adminpanel/admin_pd.html', context)

def delete_product(request, product_id):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully")
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist")
    
    return redirect('adminpanel:adminpd')
# Create your views here.

def update_product(request, product_id):
    if not AdminUser.objects.filter(user=request.user).exists():
        return redirect('login')
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist")
        return redirect('adminpanel:adminpd')

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
        return redirect('adminpanel:adminpd')

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