from django.contrib import admin

# Register your models here.
from .models import Product, Brand, Category, CatItem, Image, Package, PackageItem

from .models import ProductAdmin, PackageAdmin

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(CatItem)
admin.site.register(Image)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageItem)
