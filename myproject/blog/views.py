from django.shortcuts import render

from main_page.models import Gallery

from .models import Blogs, Tag


# Create your views here.
def blog_single(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery
    }
    return render(request, 'html_files/blog-single.html',context)

def blog(request):
    gallery = Gallery.objects.all()
    blog = Blogs.objects.all()
    tag = Tag.objects.all()
    context = {
        'gallery': gallery,
        'blog':blog,
        'tag':tag
    }
    return render(request, 'html_files/blog.html',context)


