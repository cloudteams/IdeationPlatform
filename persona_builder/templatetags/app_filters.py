# -*- coding: utf-8 -*-
import json

from django.utils.safestring import mark_safe

from persona_builder.models import PersonaUsers

__author__ = 'dimitris'

from django import template
from django.conf import settings

register = template.Library()


# logic
@register.filter
def eq(a, b):
    return a == b


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
        return mark_safe('"%s"' % ','.join([v for v in value if v is not None]))
    else:
        return value


# make lists distinct
@register.filter
def distinct(value):
    if type(value) == list:
        return list(set(value))
    else:
        return value


# get possible options for a filter ordered according to its type
@register.filter
def process_options(f):
    if not f['has_options']:
        return None

    if f['name'] == 'experience_in_platform':
        rs = ['New User', 'Experienced User', 'Veteran', ]
        result = [(r, r) for r in rs]
    elif f['name'] == 'activity_start':
        rs = ['Morning', 'Noon', 'Afternoon', 'Evening', 'Night', ]
        result = [(r, r) for r in rs]
    else:
        result = sorted(f['get_options'], key=lambda t: t[1])

    if not result or result[0][0]:
        result = [('', '')] + result

    return result


@register.filter
def count_users(persona):
    return PersonaUsers.objects.filter(persona_id=persona.pk).count()


@register.filter
def no_underscore(text):
    return text.replace('_', ' ').replace('null', 'None / Unknown')


@register.filter
def get_user_info(persona_user):
    return json.loads(persona_user.info)


@register.filter
def filterable(filter):
    return filter['name'] not in ['first_name', 'last_name', ]


@register.filter
def get_percentage(value, total):
    if total == 0:
        return 0

    return round(float(value)/total, 2)*100


@register.filter
def get_percentage_for_chart(value, total):
    if total == 0:
        return 0

    result = round(float(value)/total, 4)*100 - 0.1
    return result if result >= 0 else 0


@register.filter
def get_total(values):
    total = 0

    for v in values:
        total += v[1]

    return total
