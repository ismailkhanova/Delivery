from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.shortcuts import reverse


# class Deliveryman(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
#     phone = models.CharField(max_length=255, verbose_name='Номер телефона')
#     avatar = models.ImageField(upload_to="del_avatars/", verbose_name="Аватар", null=True,
#                                blank=True)  # нужно переделать потом null на False,
#     # добавить картинку по умолчанию
#     mini_avatar = ImageSpecField(source="avatar", processors=[ResizeToFill(100, 50)],
#                                  format="JPEG", options={"quality": 80})
#
#     def __str__(self):
#         name = str(self.user)
#         return name
#
#     class Meta:
#         verbose_name = "Курьер"
#         verbose_name_plural = "Курьеры"
#
#
# class Customer(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
#     avatar = models.ImageField(upload_to="cus_avatars/", verbose_name="Аватар", blank=True,
#                                default="cus_avatars/no-image.png")
#     mini_avatar = ImageSpecField(source="avatar", processors=[ResizeToFill(100, 50)],
#                                  format="JPEG", options={"quality": 80})
#     phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Номер телефона')
#     address = models.TextField(null=True, blank=True, verbose_name="Адрес")
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         verbose_name = "Заказчик"
#         verbose_name_plural = "Заказчики"


class Store(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, db_index=True)
    desc = models.CharField(max_length=255, verbose_name="Описание")
    avatar = models.ImageField(upload_to="store_avatars/", verbose_name="Аватар", blank=True,
                               default="store_avatars/no-image.jpg")
    mini_avatar = ImageSpecField(source="avatar", processors=[ResizeToFill(200, 100)],
                                 format="JPEG", options={"quality": 100})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мазазин"
        verbose_name_plural = "Магазины"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, db_index=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Магазин")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Магазин")
    price = models.DecimalField(decimal_places=2, max_digits=19, verbose_name="Цена")
    desc = models.CharField(max_length=255, verbose_name="Описание")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to="products_pic/", verbose_name="Картинка", blank=True,
                                default="products_pic/no-image.jpg")
    mini_picture = ImageSpecField(source="picture", processors=[ResizeToFill(800, 600)],
                                 format="JPEG", options={"quality": 100})

    def get_add_to_cart_url(self):
        return reverse("products:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("products:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    amount = models.IntegerField(default=1, verbose_name="Количество")
    ordered = models.BooleanField(default=False)

    def get_total_item_price(self):
        return self.amount * self.product.price

    def get_final_price(self):
        return self.get_total_item_price()

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Заказанный продукт"
        verbose_name_plural = "Заказанные продукты"


class Order(models.Model):
    STATUS = (
        ('Новый', 'Новый заказ'),
        ('В ожидании', 'Заказ в ожидании'),
        ('Выполнен', 'Выполненный заказ')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(OrderProduct, verbose_name="Продукты")
    created_date = models.DateTimeField(verbose_name="Дата")
    status = models.CharField(max_length=16, default='Новый', choices=STATUS, verbose_name="Статус")
    ordered = models.BooleanField(default=False, verbose_name="Заказано")

    def get_total(self):
        total = 0
        for product in self.products.all():
            total += product.get_final_price()
        return total

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

# picture = Deliveryman.objects.all()[0]
# print(picture.mini_avatar.url)
# print(picture.mini_avatar.width)

# picture = Customer.objects.all()[0]
# print(picture.mini_avatar.url)
# print(picture.mini_avatar.width)

# str = Store.objects.all()[0]
# print(str.mini_avatar.url)
# print(str.mini_avatar.width)
#
# picture = Product.objects.all()[0]
# print(picture.mini_picture.url)
# print(picture.mini_picture.width)
