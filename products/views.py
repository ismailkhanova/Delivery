from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Store, Product, Category


class StoreList(ListView):
    model = Store
    template_name = 'products/store_list.html'
    context_object_name = 'store'


class StoreProduct(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.store = get_object_or_404(Store, pk=self.kwargs['pk'])
        return Product.objects.filter(store=self.store)

    def get_context_data(self, **kwargs):
        context = super(StoreProduct, self).get_context_data(**kwargs)
        context["cat_bar"] = Category.objects.all()
        context["store_products"] = self.store
        return context


class ProductCategory(ListView):
    model = Product
    template_name = 'products/categories.html'
    context_object_name = 'pro_list'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_bar"] = Category.objects.all()
        return context
