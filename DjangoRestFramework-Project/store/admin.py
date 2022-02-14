from django.contrib import admin
from store.models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["name","price","description"]

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display=["name","address","TAX_RATE"]

@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display=["quantity","get_product_name"]

    def get_product_name(self,instance):
        return instance.product.name
