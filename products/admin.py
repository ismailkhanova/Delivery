from django.contrib import admin

from products.models import Deliveryman, Customer, Store, Category, Product, Order, OrderProduct



admin.site.register(Deliveryman)

admin.site.register(Customer)

admin.site.register(Store)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'store', 'price', 'available', 'picture', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)

admin.site.register(Order)

admin.site.register(OrderProduct)

