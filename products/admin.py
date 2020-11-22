from django.contrib import admin
from .models import Deliveryman, Customer, Store, Category, Product, OrderProduct, Order

admin.site.register(Deliveryman)
admin.site.register(Customer)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
