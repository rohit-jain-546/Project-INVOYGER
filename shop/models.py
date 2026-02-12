from django.db import models
from django.contrib.auth.models import User 
from adminpanel.models import Product

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username} created on {self.created_at}"
    

class cartitem(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart of {self.cart.user.username}"    
# Create your models here.
