from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'location', 'created_at')
    list_filter = ('categories', 'created_at')
    search_fields = ('title', 'description')

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(ReviewComment)