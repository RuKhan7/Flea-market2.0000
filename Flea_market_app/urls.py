from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]