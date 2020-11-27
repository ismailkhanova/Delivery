from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Store, Product, Category, OrderProduct, Order
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


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


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'products/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "У вас нет активного заказа")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(user=request.user, product=product)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # если продукт уже есть в заказе
        if order.products.filter(product__slug=product.slug).exists():
            order_product.amount += 1
            order_product.save()
            messages.info(request, "Количество продукта в вашей корзине обновлено.")
            return redirect("products:order-summary")
        else:
            order.products.add(order_product)
            messages.info(request, "Продукт был добавлен в вашу корзину.")
            return redirect("products:order-summary")
    else:
        order = Order.objects.create(user=request.user, created_date=timezone.now())
        order.products.add(order_product)
        messages.info(request, "Продукт был добавлен в вашу корзину.")
        return redirect("products:order-summary")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # если продукт есть в заказе
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(user=request.user, product=product, ordered=False)[0]
            order.products.remove(order_product)
            order_product.delete()
            messages.info(request, "Продукт был удалён с вашей корзины.")
            return redirect("products:order-summary")
        else:
            messages.info(request, "Этого продукта нет в вашей корзине.")
            return redirect("products:product", slug=slug)
    else:
        messages.info(request, "У вас нет активного заказа")
        return redirect("products:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # если продукт есть в заказе
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(user=request.user, product=product, ordered=False)[0]
            if order_product.amount > 1:
                order_product.amount -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
                order_product.delete()
            messages.info(request, "Количество продукта в вашей корзине обновлено.")
            return redirect("products:order-summary")
        else:
            messages.info(request, "Этого продукта нет в вашей корзине.")
            return redirect("products:product", slug=slug)
    else:
        messages.info(request, "У вас нет активного заказа")
        return redirect("products:product", slug=slug)
