from django.contrib import admin
from .models import User, Product, ProductBought

admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductBought)
