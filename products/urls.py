from django.urls import path
from .views import StoreList, StoreProduct, ProductCategory

urlpatterns = [
    path("", StoreList.as_view(), name="store_list"),
    path("store/<int:pk>/", StoreProduct.as_view(), name="store_products"),
    path("cat/<int:pk>/", ProductCategory.as_view(), name="product_category"),
    ]
