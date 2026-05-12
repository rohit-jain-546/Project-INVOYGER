from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Order, OrderItem
from adminpanel.models import Product
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
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    # Calculate subtotal (sum of all line_totals)
    order.subtotal = sum(item.line_total for item in order.items.all())
    
    # Tax calculation (18%)
    order.tax_rate = 18
    order.tax_amount = round((order.subtotal * order.tax_rate) / 100, 2)
    
    # Note: If your total_amount in DB already includes tax, use it as is
    # If not, calculate: order.total_amount = order.subtotal + order.tax_amount
    
    # Add status timestamps dynamically based on current status
    # These won't persist to DB but will be available in template
    if order.status in ['PROCESSING', 'COMPLETED', 'CANCELLED']:
        order.payment_confirmed_at = order.created_at
    
    if order.status in ['PROCESSING', 'COMPLETED', 'CANCELLED']:
        order.processing_at = order.created_at
    
    if order.status == 'COMPLETED':
        order.shipped_at = order.created_at
        order.out_for_delivery_at = order.created_at
        order.delivered_at = order.created_at
    
    if order.status == 'CANCELLED':
        order.cancelled_at = order.created_at
    
    # # Get related products (4 random products excluding items in current order)
    # ordered_product_ids = order.items.values_list('product_id', flat=True)
    # related_products = Product.objects.exclude(id__in=ordered_product_ids)[:4]
    
    # # If not enough products, get any 4 products
    # if related_products.count() < 4:
    #     related_products = Product.objects.all()[:4]
    
    context = {
        'order': order,
        # 'related_products': related_products,
    }
    
    return render(request, 'shop/order_success.html', context)

@login_required
def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return generate_invoice(order)
