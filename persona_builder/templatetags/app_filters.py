
__author__ = 'dimitris'

from django import template
from django.conf import settings

register = template.Library()


# logic
@register.filter
def get_property(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None


# printing lists nicely
@register.filter
def pretty_print(value):
    if value is None:
        return ''
    elif type(value) == list:
        result = ''
        for var in value:
            result += str(var) + '\n'
    else:
        return value

