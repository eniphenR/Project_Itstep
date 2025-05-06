from django.contrib import admin
from .models import Tovars, Size, Type, Tag, Skidka_Tovar, Gallery, Say, Get_Contatc, Contact, Carts_order, Order, \
    CartItem

admin.site.register(Tovars)
admin.site.register(Size)
admin.site.register(Type)
admin.site.register(Tag)
admin.site.register(Skidka_Tovar)
admin.site.register(Gallery)
admin.site.register(Say)
admin.site.register(Contact)
admin.site.register(Get_Contatc)
admin.site.register(Carts_order)
admin.site.register(Order)
admin.site.register(CartItem)
