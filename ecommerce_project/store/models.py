from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True, default='DEFAULT_SKU')  # Add default here
    name = models.CharField(max_length=255, default='Unnamed Product')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True, default='products/default.jpg')

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer.user.username}'s cart"

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.user.username}'s wishlist"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.customer.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, default=1)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

class Shipment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)
    shipment_date = models.DateTimeField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Shipment for Order {self.order.id}"
