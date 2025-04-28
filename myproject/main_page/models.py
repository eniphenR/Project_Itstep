from django.db import models
from django.utils.text import slugify


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
    type = models.ManyToManyField(Type,verbose_name='вид')
    tag = models.ManyToManyField(Tag,verbose_name='теги')


    def __str__(self):
        return self.name






