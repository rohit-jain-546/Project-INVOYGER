from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Order, OrderItem
from shop.utils import get_cart_for_user
from .pdf import generate_invoice
from django.shortcuts import get_object_or_404

@login_required
def checkout(request):
    cart = get_cart_for_user(request.user)
    cart_items = cart.items.all()

    if not cart_items.exists():
        return redirect('shop:cart')

    total = sum(item.total_price() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
            line_total=item.quantity * item.product.price
        )

    cart_items.delete()   
    return redirect('orders:order_success', order_id=order.order_id)
@login_required
def order_success(request, order_id):
    order = Order.objects.get(order_id=order_id, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return generate_invoice(order)
