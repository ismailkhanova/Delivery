from django.contrib import admin

from products.models import Deliveryman, Store, Category, Product, Order, OrderProduct, ApplicationForm


class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'store', 'price', 'available', 'picture', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'status']
    list_filter = ['created_date', 'status']
    search_fields = ['user__username', 'ref_code']


admin.site.register(Deliveryman)
admin.site.register(ApplicationForm)
admin.site.register(Store, StoreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)

