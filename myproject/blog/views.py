from django.shortcuts import render
from .forms import SearchForm
from main_page.models import Gallery
from .models import Blogs, Tag, Category


def blog_single(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery
    }
    return render(request, 'html_files/blog-single.html', context)


def blog(request):

    gallery = Gallery.objects.all()
    blog = Blogs.objects.all()
    tag = Tag.objects.all()
    category = Category.objects.all()

    latest_blogs = Blogs.objects.order_by('-date')[:3]

    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            blog = blog.filter(name_text__icontains=query) | blog.filter(desc__icontains=query)

    context = {
        'gallery': gallery,
        'blog': blog,
        'tag': tag,
        'category': category,
        'latest_blogs': latest_blogs,
        'form': form
    }
    return render(request, 'html_files/blog.html', context)