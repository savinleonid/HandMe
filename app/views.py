from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Profile, Category
from .forms import ProductForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




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

            # Check if a new category was entered
            new_category = request.POST.get("new_category")
            if new_category:
                category, created = Category.objects.get_or_create(name=new_category)
                product.category = category
            else:
                # Use selected category if no new category was provided
                selected_category = request.POST.get("category")
                if selected_category:
                    product.category = Category.objects.get(id=selected_category)

            product.seller = request.user
            product.save()
            return redirect("profile")
    else:
        form = ProductForm()
    categories = Category.objects.all()
    return render(request, 'app/product_form.html', {'form': form, 'categories': categories})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product = form.save(commit=False)
            new_category_name = request.POST.get('new_category')
            selected_category_id = request.POST.get('category')

            # Assign or create category
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
            elif selected_category_id:
                category = Category.objects.get(pk=selected_category_id)
            else:
                category = None

            product.category = category
            product.save()
            return redirect('profile')
    else:
        form = ProductForm(instance=product)

    categories = Category.objects.all()

    return render(request, 'app/product_edit.html', {
        'form': form,
        'product': product,
        'categories': categories,
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    product.delete()
    return redirect('profile')

def home(request):
    products = Product.objects.all()  # Default to showing all products
    query = request.GET.get('q', request.session.get('q_filter', ''))  # Get the search query from the request or session
    category_id = request.GET.get('category', request.session.get('category_filter', ''))  # Selected category ID or session
    location = request.GET.get('location', request.session.get('location_filter', ''))  # Get the selected location or session

    request.session['q_filter'] = query
    request.session['category_filter'] = category_id
    request.session['location_filter'] = location

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
        'query_filter': query,
        'category_filter': category_id,
        'location_filter': location
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

@csrf_exempt
@login_required
def profile_picture_upload(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile = request.user.profile
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        url_ = profile.profile_picture.url
        return JsonResponse({'success': True, 'new_picture_url': url_})
    return JsonResponse({'success': False})

@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()  # Deletes the user account
        logout(request)  # Logs out the user
        return redirect('home')  # Redirect to home after deletion


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
