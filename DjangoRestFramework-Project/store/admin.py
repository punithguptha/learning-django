from django.contrib import admin
from store.models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["name","price","description"]

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display=["id","name","address","TAX_RATE"]

@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display=["quantity","get_product_name","get_cart_name"]

    @admin.display(description="ProductName") #This sets the column name in the Admin DB
    def get_product_name(self,instance):
        return instance.product.name

    @admin.display(description="CartName")
    def get_cart_name(self,instance):
        return instance.shopping_cart.name or '[Guest]'
