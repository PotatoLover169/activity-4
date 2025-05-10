from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product
from .forms import ProductForm

# Create your views here.

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

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    context = {'product': product}
    return render(request, 'inventory/product_confirm_delete.html', context)
