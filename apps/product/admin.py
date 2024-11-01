from django.contrib import admin
from .models import Product


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'stock_level')
    search_fields = ('name',)
    list_filter = ('stock_level',)


admin.site.register(Product, ProductAdmin)
