from django.contrib import admin

# Register your models here.
from .models import Product, Brand, Category, CatItem, Image, Package, PackageItem

from .models import ProductAdmin, PackageAdmin, CatItemAdmin, CategoryAdmin
from .models import Chanel, Content, Meta


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CatItem, CatItemAdmin)
admin.site.register(Image)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageItem)


admin.site.register(Chanel)
admin.site.register(Content)
admin.site.register(Meta)

