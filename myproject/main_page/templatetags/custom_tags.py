from django import template

register = template.Library()

@register.filter
def get_discount(skidka_tovars, tovar):
    for skidka in skidka_tovars:
        if tovar in skidka.old.all():
            return skidka
    return None