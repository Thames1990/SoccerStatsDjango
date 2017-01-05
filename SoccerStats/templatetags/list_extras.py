from django import template

register = template.Library()


@register.filter
def filter_at_index(ls, index):
    return ls[index]
