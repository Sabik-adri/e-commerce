from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),

    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('products/', views.product_list, name='product_list'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),

    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('category-list/', views.category_list, name='category_list'),
    
    path('profile/', views.profile, name='profile'),
    # New paths for adding to cart and wishlist
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
]
