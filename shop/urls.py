from django.urls import path 
from .views import *
app_name='shop'
urlpatterns = [
    path('', user_home, name='user_home'),
    path('cart/', cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:item_id>/', update_cart_item, name='update_cart_item'),
]
