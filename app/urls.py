from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),  # Homepage for the app
    path('products/', product_list, name='product_list'),  # List of products
    path('product/<int:pk>/', product_detail, name='product_detail'),  # Detail view for a product
    path('register/', register_view, name='register'),
    path('product_create/', product_create, name='product_create'),
    path('profile/', profile_view, name='profile'),

]
