from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, View, FormView
from .models import Store, Product, Category, Order, Deliveryman, ApplicationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from products.forms import OrderForm, DeliveryForm


# страница с магазинами
class StoreList(ListView):
    model = Store
    template_name = 'products/store_list.html'
    context_object_name = 'stores'


# категории в магазинах
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


# продукты в магазине
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


# детали продукта
class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"


# корзина
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


# страница с формой для оформления заказа
class OrderFormView(LoginRequiredMixin, FormView):
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
                messages.warning(self.request, "Спасибо за оформление заказа!")
                return redirect("products:store_list")
            messages.warning(self.request, "Удостоверьтесь что вы заполнили всё правильно.")
            return redirect("products:order")
        except ObjectDoesNotExist:
            messages.warning(self.request, "У вас нет активного заказа.")
            return redirect("products:order-summary")


# страница с уже оформленными заказами (для курьеров)
class OrderedList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    permission_required = 'products.view_orders_page'
    template_name = 'products/ordered.html'
    context_object_name = 'ordered_list'

    def get_queryset(self):
        if Deliveryman.objects.filter(user=self.request.user).exists():
            return Order.objects.filter(ordered=True, deliveryman=None).exclude(user=self.request.user)
        else:
            return Order.objects.filter(ordered=True, deliveryman=None)


# детали заказа
class OrderDetail(DetailView):
    model = Order
    context_object_name = "order"


# страница с уже оформленными заказами (для заказчиков)
class OrderCustomerList(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'products/order_customer_list.html'
    context_object_name = 'ordered_list'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, ordered=True)


# страница с активными заказами (для курьеров)
class DeliveryRunningOrderList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'products/running_order_list.html'
    permission_required = 'products.view_orders_page'
    context_object_name = 'take_order_list'

    def get_queryset(self):
        if Deliveryman.objects.filter(user=self.request.user).exists():
            deliveryman = Deliveryman.objects.get(user=self.request.user)
            return Order.objects.filter(deliveryman=deliveryman)


# поиск
class SearchProductsView(ListView):
    model = Product
    template_name = 'products/search_products.html'
    context_object_name = 'search_products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search_products = Product.objects.filter(
            Q(name__icontains=query) | Q(price__icontains=query)
        )
        return search_products


# страница с формой на становление курьером
class DeliveryFormView(LoginRequiredMixin, FormView):
    template_name = 'products/delivery_form.html'
    form_class = DeliveryForm
    success_url = reverse_lazy('products:store_list')

    def get(self, *args, **kwargs):
        try:
            form = DeliveryForm()
            context = {
                'form': form
            }
            return render(self.request, "products/delivery_form.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Произошла ошибка, попробуйте сново.")
            return redirect("products:store_list")

    def post(self, *args, **kwargs):
        form = DeliveryForm(self.request.POST or None)
        try:
            if not ApplicationForm.objects.filter(user=self.request.user).exists():
                application_form = ApplicationForm.objects.create(user=self.request.user)
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    phone = form.cleaned_data.get('phone')
                    reason = form.cleaned_data.get('reason')
                    if name and phone and reason:
                        application_form.name = name
                        application_form.phone = phone
                        application_form.reason = reason
                        application_form.save()
                    else:
                        messages.warning(self.request, "Заполните все поля.")
                        return redirect("products:delivery-form")
                    messages.warning(self.request, "Спасибо, ожидайте ответа!")
                    return redirect("products:store_list")
                else:
                    messages.warning(self.request, "Удостоверьтесь что вы заполнили всё правильно.")
                    return redirect("products:delivery-form")
            else:
                messages.warning(self.request, "Вы уже подали заявку, ждите ответа.")
                return redirect("products:delivery-form")
        except ObjectDoesNotExist:
            messages.warning(self.request, "Произошла ошибка, попробуйте сново.")
            return redirect("products:store_list")


# страница с запросами на становление курьером (для стаффа)
class DeliveryAppList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ApplicationForm
    permission_required = 'products.view_app_page'
    template_name = 'products/delivery_app_list.html'
    context_object_name = 'app_list'

    def get_queryset(self):
        return ApplicationForm.objects.filter(status="В ожидании")
