from django.contrib import admin

from .models import (
    Supplier,
    Recipient,
    Location,
    Section,
    Product,
    Order,
    Delivery,
    ProductVariant,
    VariantOption,
    ProductNumber,
)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']


class RecipientAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Location)
admin.site.register(Section)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(ProductVariant)
admin.site.register(VariantOption)
admin.site.register(ProductNumber)
