from django.db import models
from django.db.models import ManyToManyField
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='Назва')
    slug = models.SlugField(unique=True, blank=True)


    def save(self, *args, **kwargs):
        if self.name and not self.name.startswith('#'):
            self.name = f'#{self.name}'

        if not self.slug:
            self.slug = slugify(self.name.lstrip('#'))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'



class Size(models.Model):
    size = models.CharField(verbose_name='розмір')

    def __str__(self):
        return self.size

class Type(models.Model):
    type = models.CharField(verbose_name='для кого')

    def __str__(self):
        return self.type


class Tovars(models.Model):
    name = models.TextField(max_length=30,verbose_name='назва')
    price = models.IntegerField(verbose_name='ціна')
    desc = models.TextField(max_length=1000,verbose_name='опис')
    manufacter = models.TextField(max_length=1000,verbose_name='мануфактура')
    img = models.ImageField(verbose_name='фото товару')

    sizes = models.ManyToManyField(Size,verbose_name='розміри',blank=True)
    type = models.ForeignKey(Type,verbose_name='вид', on_delete=models.CASCADE,blank=True,null=True)
    tag = models.ManyToManyField(Tag,verbose_name='теги')
    avaible = models.IntegerField(verbose_name='кількість',null=True)

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        """Возвращает цену со скидкой, если она есть"""
        try:
            # Проверяем, есть ли скидка на товар
            skidka = Skidka_Tovar.objects.get(old=self)
            return skidka.price_new  # Возвращаем новую цену со скидкой
        except Skidka_Tovar.DoesNotExist:
            return self.price  # Если скидки нет, возвращаем обычную цену


class Skidka_Tovar(models.Model):
    price_new = models.IntegerField(verbose_name='нова ціна')
    old = models.ManyToManyField(Tovars,verbose_name='товар')



class Gallery(models.Model):
    img = models.ImageField(verbose_name='фото для галлереї')


class Say(models.Model):
    name = models.CharField(max_length=30,verbose_name="ім'я")
    desc = models.TextField(max_length=200,verbose_name='опис')
    job = models.CharField(max_length=30,verbose_name='працівник')
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    adress = models.TextField(max_length=100,verbose_name='адреса',blank=True)
    phone = PhoneNumberField(region='UA',verbose_name='телефон',blank=True)
    email = models.EmailField(verbose_name='пошта',blank=True)
    website = models.URLField(verbose_name='сайт',blank=True)

    def __str__(self):
        return self.adress

class Get_Contatc(models.Model):
    name = models.TextField(max_length=100,verbose_name='адреса',blank=True)
    desc = models.TextField(max_length=300,verbose_name='телефон',blank=True)
    email = models.EmailField(verbose_name='пошта',blank=True)
    website = models.URLField(verbose_name='сайт',blank=True)

    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    tovar = models.ForeignKey(Tovars, on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveIntegerField(verbose_name='кількість', default=1)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, verbose_name='розмір')

    def get_total(self):
        """Возвращает общую цену товара с учетом количества и скидки"""
        return self.tovar.get_discounted_price() * self.quantity

    def get_total_order(self):
        return self.quantity

    def __str__(self):
        return f"{self.tovar.name} x{self.quantity}"


class Carts_order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач', null=True, blank=True)
    items = models.ManyToManyField(CartItem, verbose_name='позиції')
    created = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    street_address = models.CharField(max_length=255,null=True)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100,null=True)
    postcode = models.CharField(max_length=20,null=True)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)
    country = models.CharField(max_length=100,null=True)
    payment_method = models.CharField(max_length=100,null=True)

    status = models.CharField(max_length=50, default='in_cart',null=True)

    def total_price(self):
        return sum(item.get_total() for item in self.items.all())

    def __str__(self):
        return f"Кошик #{self.id} ({self.items.count()} товарів)"





class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Нове замовлення'),
        ('processing', 'Обробка'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
    )

    cart = models.ForeignKey(Carts_order, on_delete=models.CASCADE, verbose_name='Кошик', null=True, blank=True, default=None)  # Додаємо значення за замовчуванням
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=50, verbose_name='Ім’я', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Прізвище', null=True)
    country = models.CharField(max_length=100, verbose_name='Країна', null=True)
    street_address = models.TextField(verbose_name='Адреса', null=True)
    city = models.CharField(max_length=100, verbose_name='Місто', null=True)
    postcode = models.CharField(max_length=20, verbose_name='Поштовий код', null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True)
    email = models.EmailField(verbose_name='Email', null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус', null=True)

    def __str__(self):
        return f"Замовлення №{self.id} від {self.first_name} {self.last_name}"