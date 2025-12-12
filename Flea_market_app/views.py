from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def root(request):
    # Получаем 3 случайных товара для слайдов
    featured_products = Product.objects.order_by('?')[:3]
    
    category_id = request.GET.get('category')
    
    if category_id and category_id != 'all':
        products = Product.objects.filter(
            categories__id=category_id
        ).select_related('seller__user').prefetch_related('categories')
    else:
        products = Product.objects.all().select_related('seller__user').prefetch_related('categories')
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'featured_products': featured_products,  # Товары для слайдов
    }
    
    return render(request, 'main_catalog.html', context)

def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(
        Product.objects.select_related('seller__user')
        .prefetch_related('categories', 'comments', 'reviews'),
        id=product_id
    )
    
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)
featured_products = Product.objects.order_by('?')[:3]