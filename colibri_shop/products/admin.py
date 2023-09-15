from django.contrib import admin

from products.models import ProductCategory, Product, ProductBrands, Basket, Favorite

admin.site.register(ProductCategory)
admin.site.register(ProductBrands)
admin.site.register(Favorite)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('image', 'name', 'sex', 'description', ('price', 'quantity'), 'brand', 'category')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'date_created')
    readonly_fields = ('date_created',)
    extra = 0
