from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product
from .forms import ProductForm

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'inventory/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

@login_required(login_url='login')
def product_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(quantity__icontains=search_query)
        )
    else:
        products = Product.objects.all()
    
    context = {'products': products, 'search_query': search_query}
    return render(request, 'inventory/product_list.html', context)

@login_required(login_url='login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    context = {'form': form, 'title': 'Add New Product'}
    return render(request, 'inventory/product_form.html', context)

@login_required(login_url='login')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'title': 'Edit Product'}
    return render(request, 'inventory/product_form.html', context)

@login_required(login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    context = {'product': product}
    return render(request, 'inventory/product_confirm_delete.html', context)
