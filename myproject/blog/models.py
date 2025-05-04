from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(verbose_name="ім`я",max_length=15)

    def __str__(self):
        return self.name

    def category_count(self):
        return self.blogs_set.count()


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



class User(models.Model):
    name = models.CharField(verbose_name="ім`я",max_length=15)
    desc = models.TextField(verbose_name='опис',max_length=400)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey('Blogs', on_delete=models.CASCADE, related_name='comments',blank=True, null=True)
    name = models.CharField(verbose_name="ім'я користовувача",max_length=30)
    email = models.EmailField(verbose_name='почта')
    image = models.ImageField(blank=True, null=True,verbose_name='фото')
    desc = models.TextField(blank=True, null=True,verbose_name='опис')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Blogs(models.Model):
    name_text = models.CharField(verbose_name='назва блогу', max_length=70)
    desc = models.TextField(verbose_name='опис не повний')
    desc_all = models.TextField(verbose_name='опис повний',blank=True)
    comment = models.ManyToManyField(Comment,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    img = models.ImageField(verbose_name='картинка', blank=True, null=True)
    category = models.ManyToManyField(Category)

    def comment_count(self):
        return self.comment.count()



    def __str__(self):
        return self.name_text
