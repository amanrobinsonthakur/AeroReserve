from django import template

register = template.Library()


@register.filter
def split(value, key):

    return value.split(key)


@register.filter
def index(indexable, i):

    return indexable[i]