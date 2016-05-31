__author__ = 'dimitris'

from django import template

register = template.Library()


@register.filter
def get_entries(bmc, section):
    return bmc.entries.filter(section=section).order_by('created')
