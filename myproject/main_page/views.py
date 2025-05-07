from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tovars, Skidka_Tovar, Gallery, Say, Contact, Get_Contatc, Type, Tag, CartItem, Size, Carts_order, \
    Order
from django.contrib.auth.models import User

def get_tovars(qs=None):
    """
    Разбивает переданный QuerySet на четыре примерно равные части.
    Если qs=None, берёт все товары.
    """
    if qs is None:
        qs = Tovars.objects.all()
    total = qs.count()
    fourth, rem = divmod(total, 4)

    c1 = fourth + (1 if rem > 0 else 0)
    c2 = c1    + (1 if rem > 1 else 0)
    c3 = c2    + (1 if rem > 2 else 0)

    return {
        'cat1': qs[:c1],
        'cat2': qs[c1:c2],
        'cat3': qs[c2:c3],
        'cat4': qs[c3:],
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

    gallery = Gallery.objects.all()
    skidki = Skidka_Tovar.objects.prefetch_related('old').all()
    for tovar in tovars:
        tovar.discounted_price = get_discounted_tovar(tovar)

    a = Say.objects.all()

    context = {
        'tovars': tovars,
        'skidki': skidki,
        'gallery':  gallery,
        'a':a
    }

    context.update(get_tovars())
    context.update(get_skidka())

    return render(request, 'html_files/index.html', context)


def shop(request):
    gallery = Gallery.objects.all()
    type1 = get_object_or_404(Type, id=1)
    type2 = get_object_or_404(Type, id=2)

    tovars = Tovars.objects.exclude(name__exact='')


    tag_filter = request.GET.get('tag')
    if tag_filter:
        tovars = tovars.filter(tag__slug=tag_filter)


    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    if price_from:
        try:
            tovars = tovars.filter(price__gte=float(price_from))
        except ValueError:
            pass
    if price_to:
        try:
            tovars = tovars.filter(price__lte=float(price_to))
        except ValueError:
            pass


    cat_all = Tag.objects.filter(tovars__in=Tovars.objects.all()).distinct()

    skidki = Skidka_Tovar.objects.prefetch_related('old').all()
    for tovar in tovars:
        tovar.discounted_price = get_discounted_tovar(tovar)

    context = {
        'gallery': gallery,
        'type1': type1,
        'type2': type2,
        'cat_all': cat_all,  # Теги для всех товаров
        'price_from_selected': price_from or '',
        'price_to_selected': price_to or '',
        'tovars': tovars,  # Отображаем товары, которые прошли фильтрацию
        'skidki': skidki,

    }
    context.update(get_skidka())

    return render(request, 'html_files/shop.html', context)


from django.shortcuts import get_object_or_404

def product_single(request, name):
    gallery = Gallery.objects.all()
    tovars = Tovars.objects.get(name=name)


    skidki = Skidka_Tovar.objects.prefetch_related('old').all()
    tovars.discounted_price = get_discounted_tovar(tovars)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        size = request.POST.get('size')

        if quantity and size:
            size_instance = get_object_or_404(Size, size=size)


            cart_item = CartItem.objects.create(
                tovar=tovars,
                quantity=int(quantity),
                size=size_instance
            )

            cart, created = Carts_order.objects.get_or_create(user=request.user)


            cart.items.add(cart_item)


            cart.save()

            return redirect('main_page:cart')

    context = {
        'gallery': gallery,
        'tovars': tovars,
        'skidki': skidki,
    }
    context.update(get_skidka())

    return render(request, 'html_files/product-single.html', context)

def cart(request):
    order = CartItem.objects.all()
    gallery = Gallery.objects.all()

    total_sum = sum(item.get_total() for item in order)
    cart_count = sum(item.quantity for item in order)

    context = {
        'gallery': gallery,
        'order': order,
        'total_sum': total_sum,
        'cart_count': cart_count,
    }

    return render(request, 'html_files/cart.html', context)


class OrderItem:
    pass


@login_required
def checkout(request):
    # Получаем галерею товаров (если она нужна)
    gallery = Gallery.objects.all()

    # Получаем товары в корзине для текущего пользователя
    cart_items = CartItem.objects.filter(user=request.user)

    # Вычисляем общую сумму
    total_sum = sum(item.get_total() for item in cart_items)

    # Если запрос POST (оформление заказа)
    if request.method == 'POST':
        # Извлекаем данные из формы
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        street_address = request.POST.get('streetaddress')
        apartment = request.POST.get('apartment', '')
        city = request.POST.get('towncity')
        postcode = request.POST.get('postcodezip')
        phone = request.POST.get('phone')
        email = request.POST.get('emailaddress')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')

        # Создаем новый заказ Carts_order
        order = Carts_order.objects.create(
            first_name=first_name,
            last_name=last_name,
            street_address=street_address,
            apartment=apartment,
            city=city,
            postcode=postcode,
            phone=phone,
            email=email,
            country=country,
            payment_method=payment_method,
            user=request.user  # Связь с текущим пользователем
        )

        # Добавляем товары из корзины в заказ
        for item in cart_items:
            OrderItem.objects.create(
                order=order,  # Связь с заказом
                product=item.tovar,  # Ссылка на товар
                quantity=item.quantity,
                price=item.tovar.get_discounted_price()  # Цена со скидкой
            )

        # Удаляем товары из корзины
        cart_items.delete()

        # Создаем объект Order для отслеживания статуса
        new_order = Order.objects.create(
            cart=order,  # Связь с корзиной
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            street_address=street_address,
            city=city,
            postcode=postcode,
            phone=phone,
            email=email,
            country=country,
            status='new',  # Новый заказ
        )

        # Перенаправляем на страницу успешного оформления заказа
        return redirect('main_page:order_succes')

    context = {
        'gallery': gallery,
        'total_sum': total_sum,
    }

    return render(request, 'html_files/checkout.html', context)



def about(request):
    gallery = Gallery.objects.all()

    a = Say.objects.all()
    context = {
        'gallery': gallery,
        'a':a,
    }

    return render(request, 'html_files/about.html',context)



def contact(request):
    gallery = Gallery.objects.all()
    contact = Contact.objects.first()
    get_contact = Get_Contatc.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        desc = request.POST.get('desc')
        if name and email and website and desc:
            Get_Contatc.objects.create(
                name=name,
                email=email,
                website=website,
                desc=desc
            )
            return redirect('main_page:contact')  # или на любую другую страницу



    context = {
        'gallery': gallery,
        'contact':contact
    }

    return render(request, 'html_files/contact.html',context)


def remove_item(request, item_id):

    item = get_object_or_404(CartItem, id=item_id)
    item.delete()


    return redirect('main_page:cart')


def order_succes(request):
    return render(request, 'html_files/order_succes.html')