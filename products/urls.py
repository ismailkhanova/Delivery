from django.urls import path
from .views import StoreList, StoreProduct, ProductCategory, ProductDetail

urlpatterns = [
    path("", StoreList.as_view(), name="store_list"),
    path("store/<slug>/", StoreProduct.as_view(), name="store_products"),
    path("cat/<slug>/", ProductCategory.as_view(), name="product_category"),
    path("<int:pk>/", ProductDetail.as_view(), name="product_detail"),
    ]
