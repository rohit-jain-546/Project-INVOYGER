from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Customer
from adminpanel.models import Product
from django.contrib.auth.decorators import login_required

from orders.models import Order
from shop.utils import get_cart_for_user
from .models import cartitem

@login_required(login_url='/login/')
def user_home(request):
    if not Customer.objects.filter(user=request.user).exists():
        return redirect('login')
    q=Product.objects.all()[:4]
    context={'products':q}

    return render(request, 'shop/home.html', context)
@login_required(login_url='/login/')
def cart_view(request):
    cart=get_cart_for_user(request.user)
    
    items = cart.items.all()

    total=sum([item.total_price() for item in items])
    
    context={'cart_items':items, 'total':total}

    return render(request, 'shop/cart.html', context)

# Create your views here.
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    cart=get_cart_for_user(request.user)
    product=get_object_or_404(Product   ,  id=product_id)

    cart_item, created=cartitem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('shop:cart_view')    

def remove_from_cart(request, item_id):
    cart_item=get_object_or_404(cartitem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('shop:cart_view')

def update_cart_item(request, item_id):
    
    if request.method == "POST":
        item = get_object_or_404(cartitem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get("quantity", 1))
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
           
    return redirect('shop:cart_view')

def products_view(request):
    products = Product.objects.filter(category__in=["M", "U"])

    context={'products':products}
    return render(request, 'shop/products.html', context)

def public_home(request):
    q=Product.objects.all()[:4]
    context={'products':q}
    return render(request, 'shop/public_home.html', context)

def Wp_view(request):
    products = Product.objects.filter(category__in=["W", "U"])

    context={'products':products}
    return render(request, 'shop/wpd.html', context)
def accessory_view(request):
    products = Product.objects.filter(category__in=["AS", "U"])

    context={'products':products}
    return render(request, 'shop/accessory.html', context)
def kids_view(request):
    products = Product.objects.filter(category__in=["K", "U"])

    context={'products':products}
    return render(request, 'shop/kids.html', context)

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "shop/orders.html", {"orders": orders})