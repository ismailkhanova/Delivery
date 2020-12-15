from django.urls import path
from .views import (StoreList, ProductCategory, ProductDetail, StoreProduct
, OrderSummaryView, add_to_cart, remove_from_cart, remove_single_item_from_cart
, OrderFormView, OrderedList, OrderCustomerList, take_order, DeliveryRunningOrderList
, remove_order, SearchProductsView, DeliveryFormView, DeliveryAppList, accept_app
, refuse_app, confirm_execution)

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
    path("my_orders/", OrderCustomerList.as_view(), name="order_owner_list"),
    path("orders_taken/", DeliveryRunningOrderList.as_view(), name="orders_taken"),
    path("take-order/<int:pk>/", take_order, name="take-order"),
    path("remove-order/<int:pk>/", remove_order, name="remove-order"),
    path('search/', SearchProductsView.as_view(), name='search_products'),
    path("delivery-form/", DeliveryFormView.as_view(), name="delivery-form"),
    path("app-list/", DeliveryAppList.as_view(), name="app-list"),
    path("accept_app/<int:pk>/", accept_app, name="accept_app"),
    path("refuse_app/<int:pk>/", refuse_app, name="refuse_app"),
    path("confirm_execution/<int:pk>/", confirm_execution, name="confirm_execution"),
]
