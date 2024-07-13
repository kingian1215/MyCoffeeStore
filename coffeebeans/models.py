from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def product_image_path(instance, filename):
    # 文件将上传到 MEDIA_ROOT/product/<filename>
    return f'./media/product/{filename}'

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_path, default='default.jpg')
    introduce = models.TextField(max_length=500)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem', related_name='carts')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=0)


# class Order(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

#     def calculate_total_price(self):
#         # Calculate total price based on OrderItems
#         total = sum(item.product.price * item.quantity for item in self.order_items.all())
#         print(total)
#         return total

#     def save(self, *args, **kwargs):
#         self.total_price = self.calculate_total_price()
#         # super().save(*args, **kwargs)
#         self.save()

#     def __str__(self):
#         return f"Order #{self.pk}"  

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def calculate_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.order_items.all())
        return total

    def __str__(self):
        return f"Order #{self.pk}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
