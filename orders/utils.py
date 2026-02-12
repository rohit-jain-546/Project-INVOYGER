from .models import cart

def get_cart_for_user(user):
    cart_obj, created = cart.objects.get_or_create(user=user)
    return cart_obj