from django.urls import path
from .views import StoreList

urlpatterns = [
    path("", StoreList.as_view(), name="store_list"),
    ]
