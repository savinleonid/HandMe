from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Profile, Category
from .forms import ProductForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q



def product_list(request):
    products = Product.objects.all()
    return render(request, 'app/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/product_detail.html', {'product': product})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'app/product_form.html', {'form': form})

def home(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    products = Product.objects.all()  # Default to showing all products
    category_id = request.GET.get('category', '')  # Selected category ID
    location = request.GET.get('location', '')  # Get the selected location

    # Filter products based on search query
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(location__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if location:
        products = products.filter(location=location)

    categories = Category.objects.all()

    # Fetch unique locations from the products
    locations = Product.objects.values_list('location', flat=True).distinct()

    # Fetch the user's profile picture if authenticated
    profile_picture = None
    if request.user.is_authenticated:
        profile_picture = request.user.profile.profile_picture.url

    return render(request, 'app/home.html', {
        'products': products,
        'categories': categories,
        'locations': locations,  # Pass the unique locations to the template
        'selected_category': category_id,
        'selected_location': location,  # Pass the selected location back to the template
        'profile_picture': profile_picture,
        'query': query,  # Pass the search query back to the template
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})  # Create a register.html template

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the product list or homepage
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the login page after logout


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'app/profile.html', {'form': form})
