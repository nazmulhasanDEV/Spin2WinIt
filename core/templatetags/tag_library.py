from django import template

register = template.Library()

@register.filter()
def to_float(value):
    return float(value)

@register.filter()
def count_obj(value):

    return len(value)

@register.filter()
def multiply(value):

    return value * 50