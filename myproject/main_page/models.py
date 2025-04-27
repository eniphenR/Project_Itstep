from django.db import models

# Create your models here.

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
    type = models.ManyToManyField(Type,verbose_name='вид')


    def __str__(self):
        return self.name
