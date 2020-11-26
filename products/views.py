from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Store, Product, Category


class StoreList(ListView):
    model = Store
    template_name = 'products/store_list.html'
    context_object_name = 'stores'


class ProductCategory(ListView):
    model = Category
    template_name = 'products/product_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        self.store = get_object_or_404(Store, slug=self.kwargs['slug'])
        return Category.objects.filter(store=self.store)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(store=self.store)
        return context


class StoreProduct(ListView):
    model = Product
    template_name = 'products/cat_product_list.html'
    context_object_name = 'cat_products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(store=self.category.store)
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
