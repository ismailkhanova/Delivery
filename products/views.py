from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Store


class StoreList(ListView):
    model = Store
    template_name = 'products/store_list.html'
    context_object_name = 'store'
