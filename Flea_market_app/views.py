from django.shortcuts import render
from .models import Product

def root(request):
    return render(request, 'main_catalog.html')




