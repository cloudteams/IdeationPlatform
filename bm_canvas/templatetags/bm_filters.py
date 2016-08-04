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
    return mark_safe(markdown.markdown(markdown_text, extensions=['markdown.extensions.sane_lists',
                                                                  'markdown.extensions.nl2br']))


@register.filter
def get_default_project(request):
    try:
        return request.session['project_id']
    except KeyError:
        try:
            return request.session['projects'][0]['pid']
        except KeyError:
            return None
        except IndexError:
            return None
