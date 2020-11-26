from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from inel_delivery.users.models import User


class Deliveryman(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to="del_avatars/", verbose_name="Аватар", null=True,
                               blank=True)  # нужно переделать потом null на False,
    # добавить картинку по умолчанию
    mini_avatar = ImageSpecField(source="avatar", processors=[ResizeToFill(100, 50)],
                                 format="JPEG", options={"quality": 80})

    def __str__(self):
        name = str(self.user)
        return name

    class Meta:
        verbose_name = "Курьер"
        verbose_name_plural = "Курьеры"


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to="cus_avatars/", verbose_name="Аватар", null=True,
                               blank=True)  # нужно переделать потом null на False,
    # добавить картинку по умолчанию
    mini_avatar = ImageSpecField(source="avatar", processors=[ResizeToFill(100, 50)],
                                 format="JPEG", options={"quality": 80})
    address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        name = str(self.user)
        return name

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


class Store(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, db_index=True)
    desc = models.CharField(max_length=255, verbose_name="Описание")
    avatar = models.ImageField(upload_to="store_avatars/", verbose_name="Аватар", null=False,
                               blank=True, default="store_avatars/no-image.jpg")
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
    picture = models.ImageField(upload_to="products_pic/", verbose_name="Картинка", null=False,
                               blank=True, default="products_pic/no-image.jpg")
    mini_picture = ImageSpecField(source="picture", processors=[ResizeToFill(800, 600)],
                                 format="JPEG", options={"quality": 100})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class OrderProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Заказчик")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    amount = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        name = str(self.product)
        return name

    class Meta:
        verbose_name = "Заказанный продукт"
        verbose_name_plural = "Заказанные продукты"


class Order(models.Model):
    STATUS = (
        ('Новый', 'Новый заказ'),
        ('В ожидании', 'Заказ в ожидании'),
        ('Выполнен', 'Выполненный заказ')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Заказчик")
    products = models.ManyToManyField(OrderProduct, verbose_name="Продукты")
    deliveryman = models.ForeignKey(Deliveryman, on_delete=models.CASCADE, verbose_name="Курьер")
    date = models.DateTimeField(verbose_name="Дата", default=timezone.now)
    status = models.CharField(max_length=16, default='Новый', choices=STATUS, verbose_name="Статус")

    def __str__(self):
        order_id = str(self.id)
        return order_id

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
