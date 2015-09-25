
__author__ = 'dimitris'

from django import template
from django.conf import settings

register = template.Library()


# logic
@register.filter
def get_property(dict, key):
    if key in dict:
        return dict[key]
    else:
        return None


# printing lists nicely
@register.filter
def pretty_print(value):
    if type(value) == list:
        return ','.join(value)
    else:
        return value

