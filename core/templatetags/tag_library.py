from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return float(value)

@register.filter()
def to_float(value):
    return float(value)

@register.filter()
def count_obj(value):

    return len(value)

# for daily sign in bonus
@register.filter()
def multiply(value):

    return value * 50