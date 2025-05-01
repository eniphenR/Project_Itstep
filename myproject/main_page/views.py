from django.shortcuts import render
from .models import Tovars,Skidka_Tovar,Gallery


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



def get_skidka():
    skidka_tovars = Skidka_Tovar.objects.prefetch_related('old').all()
    return {'skidka_tovars': skidka_tovars}

def get_discounted_tovar(tovar):
    discounted_item = Skidka_Tovar.objects.filter(old=tovar).first()
    if discounted_item:
        return discounted_item.price_new
    return tovar.price

def index(request):
    tovars = Tovars.objects.all()
    skidki = Skidka_Tovar.objects.prefetch_related('old').all()
    gallery = Gallery.objects.all()
    for tovar in tovars:
        tovar.discounted_price = get_discounted_tovar(tovar)

    context = {
        'tovars': tovars,
        'skidki': skidki,
        'gallery':  gallery
    }

    context.update(get_tovars())
    context.update(get_skidka())
    return render(request, 'html_files/index.html', context)

def shop(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery':gallery
    }
    return render(request, 'html_files/shop.html',context)

def product_single(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery
    }
    return render(request, 'html_files/product-single.html',context)

def cart(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery
    }
    return render(request, 'html_files/cart.html',context)

def checkout(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery
    }
    return render(request, 'html_files/checkout.html',context)

def about(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery
    }
    return render(request, 'html_files/about.html',context)



def contact(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery
    }
    return render(request, 'html_files/contact.html',context)

