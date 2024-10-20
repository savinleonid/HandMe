from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage for the app
    path('products/', views.product_list, name='product_list'),  # List of products
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Detail view for a product
    path('product/new/', views.product_create, name='product_create'),  # View for adding a new product
]
