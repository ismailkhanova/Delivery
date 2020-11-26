from django.urls import path
from .views import StoreList, ProductCategory, ProductDetail, StoreProduct

urlpatterns = [
    path("", StoreList.as_view(), name="store_list"),
    path("store/<slug>/", ProductCategory.as_view(), name="product_category"),
    path("category/<slug>/", StoreProduct.as_view(), name="cat_products"),
    path("<int:pk>/", ProductDetail.as_view(), name="product_detail"),
    ]
