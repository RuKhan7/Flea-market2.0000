from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Message)
admin.site.register(Favorite)

