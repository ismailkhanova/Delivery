from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, View, FormView, UpdateView
from .models import Store, Product, Category, OrderProduct, Order
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from products.forms import OrderForm

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
        messages.info(request, "У вас нет активного заказа.")
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
        messages.info(request, "У вас нет активного заказа.")
        return redirect("products:product", slug=slug)


class OrderFormView(FormView):
    template_name = 'products/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('products:store_list')

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = OrderForm()
            context = {
                'form': form,
                'order': order
            }
            return render(self.request, "products/order.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "У вас нет активного заказа.")
            return redirect("products:order")

    def post(self, *args, **kwargs):
        form = OrderForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                phone = form.cleaned_data.get('phone')
                address = form.cleaned_data.get('address')
                if name and phone and address:
                    order.name = name
                    order.phone = phone
                    order.address = address
                    order.ordered = True
                    order.save()
                    order_products = order.products.all()
                    order_products.update(ordered=True)
                    for product in order_products:
                        product.save()
                else:
                    messages.warning(self.request, "Заполните все поля.")
                    return redirect("products:order")
                messages.warning(self.request, "Спасибо за оформление заказа, мы надеемся что вы не проживёте очень "
                                               "долго)")
                return redirect("products:store_list")
            messages.warning(self.request, "Удостоверьтесь что вы заполнили всё правильно.")
            return redirect("products:order")
        except ObjectDoesNotExist:
            messages.warning(self.request, "У вас нет активного заказа.")
            return redirect("products:order-summary")


class OrderedList(PermissionRequiredMixin, ListView):
    model = Order
    permission_required = 'products.view_orders_page'
    template_name = 'products/ordered.html'
    context_object_name = 'ordered_list'

    def get_queryset(self):
        return Order.objects.filter(ordered=True)


class OrderCustomerList(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'products/order_customer_list.html'
    context_object_name = 'ordered_list'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)



