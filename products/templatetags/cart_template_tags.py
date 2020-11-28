from django import template
from products.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user.id, ordered=False)
        if qs.exists():
            return qs[0].products.count()
    return 0


@register.filter
def ordered_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(ordered=True)
        if qs.exists():
            return qs.count()
    return 0
