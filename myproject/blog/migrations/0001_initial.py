# Generated by Django 5.2 on 2025-05-01 21:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name="ім'я користовувача")),
                ('email', models.EmailField(max_length=254, verbose_name='почта')),
                ('website', models.TextField(blank=True, null=True, verbose_name='вебсайт')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='опис')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Назва')),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='ім`я')),
                ('desc', models.TextField(max_length=400, verbose_name='опис')),
            ],
        ),
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=70, verbose_name='назва блогу')),
                ('desc', models.TextField(verbose_name='опис')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ManyToManyField(to='blog.comment')),
                ('tag', models.ManyToManyField(to='blog.tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user')),
            ],
        ),
    ]
