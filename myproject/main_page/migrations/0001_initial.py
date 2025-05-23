# Generated by Django 5.2 on 2025-04-27 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(verbose_name='розмір')),
            ],
        ),
        migrations.CreateModel(
            name='Tovars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=30, verbose_name='назва')),
                ('price', models.IntegerField(verbose_name='ціна')),
                ('desc', models.TextField(max_length=1000, verbose_name='опис')),
                ('manufacter', models.TextField(max_length=1000, verbose_name='мануфактура')),
                ('img', models.ImageField(upload_to='', verbose_name='фото товару')),
                ('sizes', models.ManyToManyField(blank=True, to='main_page.size', verbose_name='розміри')),
            ],
        ),
    ]
