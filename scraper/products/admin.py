from django.contrib import admin
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "price", "sku", "description")
    list_filter = ("id", "date_created")
    list_per_page = 10


admin.site.register(Product, ProductAdmin)

