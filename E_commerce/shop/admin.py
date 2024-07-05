from django.contrib import admin
from .models import product,catagory,Cart,Favourite

# Register your models here.
admin.site.register(product)
admin.site.register(catagory)
admin.site.register(Cart)
admin.site.register(Favourite)
