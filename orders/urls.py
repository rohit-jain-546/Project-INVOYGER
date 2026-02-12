from django.urls import path 
from .views import *
from .views import invoice_pdf
app_name='orders'
urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('order-success/<str:order_id>/', order_success, name='order_success'),
    path('invoice/<str:order_id>/', invoice_pdf, name='invoice_pdf'),

    ]




