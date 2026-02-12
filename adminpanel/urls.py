from django.urls import path 
from . import views
app_name = "adminpanel"

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('products/', views.adminpd, name='adminpd'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('orders/<str:order_id>/download-invoice/', views.download_invoice, name='download_invoice'),
]
