import markdown
from django.utils.safestring import mark_safe

__author__ = 'dimitris'

from django import template

register = template.Library()


@register.filter
def get_entries(bmc, section):
    return bmc.entries.filter(section=section).order_by('order')


@register.filter
def markdown_to_html(markdown_text):
    return mark_safe(markdown.markdown(markdown_text))
