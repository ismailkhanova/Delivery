from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from .models import Product, OrderProduct, Order, Deliveryman, ApplicationForm
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def add_to_cart(request, slug):
    """
    Добавляет продукт в корзину, если он там уже присутствует, то увеличивает его количество на 1.
    """
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(user=request.user, product=product, ordered=False)
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
    """
    Убирает еденицу продукта с корзины, если при этом его остаётся 0, то убирает полностью.
    """
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
    """
    Убирает продукт с корзины, в каком бы не был он количестве.
    """
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


@login_required
def take_order(request, pk):
    """
    Добавляет к заказу курьера и меняет статус заказа на 'В ожидании'.
    """
    order_pk = get_object_or_404(Order, pk=pk)
    if request.user.has_perm('products.take_orders') and Deliveryman.objects.filter(user=request.user).exists():
        order = Order.objects.get(pk=order_pk.pk)
        if not order.user == request.user:
            if order.deliveryman is None:
                deliveryman = Deliveryman.objects.get(user=request.user)
                order.deliveryman = deliveryman
                order.status = "В ожидании"
                order.save()
                messages.info(request, "Вы взяли заказ.")
                return redirect("products:orders_taken")
            else:
                messages.info(request, "Вы не можете взять этот заказ.")
                return redirect("products:ordered")
        else:
            messages.info(request, "Вы не можете взять свой заказ.")
            return redirect("products:ordered")
    else:
        messages.info(request, "У вас недостаточно прав для этого.")
        return redirect("products:ordered")


@login_required
def remove_order(request, pk):
    """
    Снимает курьера с заказа и меняет статус заказа на 'Новый'.
    """
    order_pk = get_object_or_404(Order, pk=pk)
    if request.user.has_perm('products.take_orders') and Deliveryman.objects.filter(user=request.user).exists():
        order = Order.objects.get(pk=order_pk.pk)
        order.deliveryman = None
        order.status = "Новый"
        order.save()
        messages.info(request, "Вы отказались от заказа.")
        return redirect("products:orders_taken")
    else:
        messages.info(request, "У вас недостаточно прав для этого.")
        return redirect("products:ordered")


@login_required
def confirm_execution(request, pk):
    """
       Меняет статус заказа на 'Выполнен'.
    """
    order_pk = get_object_or_404(Order, pk=pk)
    order = Order.objects.get(pk=order_pk.pk)
    if order.user == request.user:
        if order.deliveryman is not None and order.status != "Новый":
            if order.status != "Выполнен":
                if order.status == "В ожидании":
                    order.status = "Выполнен"
                    order.save()
                    messages.info(request, "Вы успешно подтвердили, что заказ выполнен.")
                    return redirect("products:order_owner_list")
                else:
                    messages.info(request, "Произошла ошибка, обратитесь в администрацию.")
                    return redirect("products:order_owner_list")
            else:
                messages.info(request, "Этот заказ уже выполнен.")
                return redirect("products:order_owner_list")
        else:
            messages.info(request, "У вашего заказа нет курьера.")
            return redirect("products:order_owner_list")
    else:
        messages.info(request, "Это не ваш заказ.")
        return redirect("products:order_owner_list")


@login_required
def accept_app(request, pk):
    """
       Принимает заявку, добавив пользователя в таблицу с курьерами и занеся его в группу 'deliveryman'.
       Меняет статус заявки на 'Принято'.
    """
    app_pk = get_object_or_404(ApplicationForm, pk=pk)
    if request.user.has_perm('accept_app'):
        app = ApplicationForm.objects.get(pk=app_pk.pk)
        if app.status == "В ожидании":
            if not Deliveryman.objects.filter(user=app.user).exists():
                app.status = "Принято"
                app.save()
                deliveryman = Deliveryman.objects.create(user=app.user)
                deliveryman.name = app.name
                deliveryman.phone = app.phone
                deliveryman.save()
                deliveryman_group = Group.objects.get(name='deliveryman')
                deliveryman_group.user_set.add(app.user)
                messages.info(request, "Вы приняли заявку.")
                return redirect("products:app-list")
            else:
                messages.info(request, "Этот пользователь уже зарегестрирован в базе данных.")
                return redirect("products:app-list")
        else:
            messages.info(request, "Эта заявка уже обработана.")
            return redirect("products:app-list")
    else:
        messages.info(request, "У вас недостаточно прав для этого.")
        return redirect("products:app-list")


@login_required
def refuse_app(request, pk):
    """
       Отказывает в заявке, поменяв статус на 'Отказано'.
    """
    app_pk = get_object_or_404(ApplicationForm, pk=pk)
    if request.user.has_perm('accept_app'):
        app = ApplicationForm.objects.get(pk=app_pk.pk)
        if app.status == "В ожидании":
            app.status = "Отказано"
            app.save()
            messages.info(request, "Вы отказали в заявке.")
            return redirect("products:app-list")
        else:
            messages.info(request, "Эта заявка уже обработана.")
            return redirect("products:app-list")
    else:
        messages.info(request, "У вас недостаточно прав для этого.")
        return redirect("products:app-list")
