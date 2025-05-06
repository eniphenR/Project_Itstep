from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

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

