from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Avg
from .models import *
from django.core.paginator import Paginator

def get_all_categories():
    return Category.objects.all()

def home(request):
    category_id = request.GET.get('category')
    city = request.GET.get('city')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    search_query = request.GET.get('q', '')
    
    products = Product.objects.filter(status='active')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if city:
        products = products.filter(city__icontains=city)
    
    if price_min:
        products = products.filter(price__gte=price_min)
    
    if price_max:
        products = products.filter(price__lte=price_max)
    
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    total_products = Product.objects.count()
    active_products = Product.objects.filter(status='active').count()
    total_categories = Category.objects.count()
    
    popular_categories = Category.objects.annotate(
        product_count=Count('product')
    ).order_by('-product_count')[:6]
    
    paginator = Paginator(products.order_by('-created_at'), 12)
    page = request.GET.get('page', 1)
    products_page = paginator.get_page(page)
    
    context = {
        'products': products_page,
        'popular_categories': popular_categories,
        'total_products': total_products,
        'active_products': active_products,
        'total_categories': total_categories,
        'all_categories': get_all_categories(),
    }
    
    return render(request, 'home.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related('seller__user', 'category'),
        id=product_id
    )
    
    product.views += 1
    product.save(update_fields=['views'])
    
    reviews = Review.objects.filter(product__seller=product.seller)
    seller_reviews = reviews.count()
    
    seller_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    context = {
        'product': product,
        'reviews': reviews,
        'seller_products_count': Product.objects.filter(seller=product.seller).count(),
        'seller_reviews': seller_reviews,
        'seller_rating': round(seller_rating, 1),
        'all_categories': get_all_categories(),
    }
    
    return render(request, 'product_detail.html', context)

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, status='active')
    
    context = {
        'category': category,
        'products': products,
        'all_categories': get_all_categories(),
    }
    
    return render(request, 'category_products.html', context)

def search(request):
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query),
            status='active'
        )
    else:
        products = Product.objects.filter(status='active')
    
    context = {
        'products': products.order_by('-created_at'),
        'query': query,
        'all_categories': get_all_categories(),
    }
    
    return render(request, 'search.html', context)

def product_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        city = request.POST.get('city')
        
        if title and price and category_id:
            category = Category.objects.get(id=category_id)
            
            first_profile = Profile.objects.first()
            if not first_profile:
                from django.contrib.auth.models import User
                user = User.objects.create_user(
                    username='demo_user',
                    password='demo_password',
                    email='demo@example.com'
                )
                first_profile = Profile.objects.create(user=user)
            
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                seller=first_profile,
                category=category,
                city=city,
                status='active'
            )
            
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('product_detail', product_id=product.id)
    
    categories = Category.objects.all()
    return render(request, 'product_create.html', {
        'categories': categories,
        'all_categories': get_all_categories(),
    })