from django.contrib import admin
from .models import Category, Product, Customer, Cart, Wishlist, Order, OrderItem, Payment, Shipment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Shipment)
