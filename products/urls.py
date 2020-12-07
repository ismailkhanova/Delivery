from django.urls import path
from .views import (StoreList, ProductCategory, ProductDetail, StoreProduct
    , OrderSummaryView, add_to_cart, remove_from_cart, remove_single_item_from_cart
    , OrderFormView, OrderedList, OrderCustomerList, SearchProductsView)

app_name = 'products'

urlpatterns = [
    path("", StoreList.as_view(), name="store_list"),
    path("store/<slug>/", ProductCategory.as_view(), name="product_category"),
    path("category/<slug>/", StoreProduct.as_view(), name="cat_products"),
    path("<int:pk>/", ProductDetail.as_view(), name="product_detail"),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", remove_from_cart, name="remove-from-cart"),
    path("remove-item-from-cart/<slug>/", remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path("order/", OrderFormView.as_view(), name="order"),
    path("ordered/", OrderedList.as_view(), name="ordered"),
    path("my", OrderCustomerList.as_view(), name="order_owner_list"),
    path('search/', SearchProductsView.as_view(), name='search_products'),
]
