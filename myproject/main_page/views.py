from django.shortcuts import render
from .models import Tovars


def get_tovars():
    all_tovars = Tovars.objects.all()
    total_count = all_tovars.count()


    fourth = total_count // 4
    remainder = total_count % 4


    cat1_end = fourth + (1 if remainder > 0 else 0)
    cat2_end = cat1_end + (1 if remainder > 1 else 0)
    cat3_end = cat2_end + (1 if remainder > 2 else 0)

    return {
        'cat1': all_tovars[:cat1_end],
        'cat2': all_tovars[cat1_end:cat2_end],
        'cat3': all_tovars[cat2_end:cat3_end],
        'cat4': all_tovars[cat3_end:]
    }

def index(request):
    tovars = Tovars.objects.all()

    context = {
        'tovars':tovars
    }

    context.update(get_tovars())
    return render(request, 'html_files/index.html',context)

def shop(request):
    return render(request, 'html_files/shop.html')

def product_single(request):
    return render(request, 'html_files/product-single.html')

def cart(request):
    return render(request, 'html_files/cart.html')

def checkout(request):
    return render(request, 'html_files/checkout.html')

def about(request):
    return render(request, 'html_files/about.html')

def blog(request):
    return render(request, 'html_files/blog.html')

def contact(request):
    return render(request, 'html_files/contact.html')