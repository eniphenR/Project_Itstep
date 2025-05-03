from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from main_page.models import Gallery
from .models import Blogs, Tag, Category


def blog_single(request,name):
    post = get_object_or_404(Blogs, name_text=name)
    blog = Blogs.objects.all()
    category = Category.objects.all()
    tag = Tag.objects.all()
    latest_blogs = Blogs.objects.order_by('-date')[:3]

    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery,
        'post':post,
        'blogs':blog,
        'category': category,
        'tag': tag,
        'latest_blogs': latest_blogs
    }
    return render(request, 'html_files/blog-single.html', context)


def blog(request):

    gallery = Gallery.objects.all()
    blogs = Blogs.objects.exclude(name_text__exact='')
    tag = Tag.objects.all()
    category = Category.objects.all()

    latest_blogs = Blogs.objects.order_by('-date')[:3]

    category_filter = request.GET.get('category', None)
    tag_filter = request.GET.get('tag', None)

    if category_filter:
        blogs = blogs.filter(category__id=category_filter)

    if tag_filter:
        blogs = blogs.filter(tag__id=tag_filter)

    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            blogs = blogs.filter(name_text__icontains=query) | blogs.filter(desc__icontains=query)

    context = {
        'gallery': gallery,
        'blogs': blogs,
        'tag': tag,
        'category': category,
        'latest_blogs': latest_blogs,
        'form': form
    }
    return render(request, 'html_files/blog.html', context)