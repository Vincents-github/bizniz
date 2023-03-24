from django import template
from django.template.defaulttags import register
import json


register = template.Library()

@register.filter
def slice_and_ellipsis(value, arg):
    length = int(arg)
    if len(value) > length:
        return value[:length] + '...'
    return value
