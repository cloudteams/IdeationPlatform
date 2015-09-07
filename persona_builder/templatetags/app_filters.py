
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

