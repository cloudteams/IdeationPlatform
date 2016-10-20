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

    result = sorted(f['get_options'], key=lambda t: t[1])
    if not result or result[0][0]:
        result = [('', '')] + result

    return result


# get the appropriate persona list title
@register.filter
def list_page_title(request):
    if 'campaign_id' in request.session:
        cid = request.session['campaign_id']
        for campaign in request.session['campaigns']:
            if campaign['cid'] == cid:
                return u'Personas in «%s» campaign' % campaign['title']

        return 'Personas in campaign with id #%s' % str(cid)
    elif 'project_id' in request.session:
        pid = request.session['project_id']
        for project in request.session['projects']:
            if project['pid'] == pid:
                return u'Personas in «%s» project' % project['title']

        return 'Personas in project with id #%s' % str(pid)
    else:
        return 'Your own & public personas'


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
def get_total(values):
    total = 0

    for v in values:
        total += v[1]

    return total
