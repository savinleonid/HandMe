from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),  # Homepage for the app
    path('products/', product_list, name='product_list'),  # List of products
    path('product/<int:pk>/', product_detail, name='product_detail'),  # Detail view for a product
    path('product/<int:pk>/edit/', product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', product_delete, name='product_delete'),
    path('register/', register_view, name='register'),
    path('product_create/', product_create, name='product_create'),
    path('profile/', profile_view, name='profile'),
    path('delete_account/', delete_account, name='delete_account'),
    path('profile/upload_picture/', profile_picture_upload, name='profile_picture_upload'),

]
