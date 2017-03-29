import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from bm_canvas.lists import BUSINESS_MODEL_SECTIONS
from bm_canvas.models import BusinessModel, BusinessModelEntry
from persona_builder.models import Persona


def project_view(request, pk):
    pk = int(pk)
    bmcs = BusinessModel.objects.filter(project_id=pk)

    project_name = ''
    for p in request.session['projects']:
        if int(p['pid']) == pk:
            project_name = p['title']
            request.session['project_id'] = str(pk)

    if not project_name:
        return HttpResponse('Access not allowed', status=403)

    return render(request, 'bm_canvas/list.html', {
        'project_id': pk,
        'project_name': project_name,
        'bmcs': bmcs,
    })


def create_canvas(request, pk):
    if request.method != 'POST':
        return HttpResponse('Only POST method allowed', status=403)

    project_name = ''
    for p in request.session['projects']:
        if p['pid'] == str(pk):
            project_name = p['title']

    if not project_name:
        return HttpResponse('Access not allowed', status=403)

    # create new bmc item
    bmc = BusinessModel.objects.create(project_id=pk, project_name=project_name, title=request.POST.get('title'))

    return redirect('/team-ideation-tools/business-model/projects/%s/%s/' % (str(pk), str(bmc.pk)))


def delete_canvas(request, pk):
    if request.method != 'POST':
        return HttpResponse('Only POST method allowed', status=403)

    project_name = ''
    for p in request.session['projects']:
        if p['pid'] == str(pk):
            project_name = p['title']

    if not project_name:
        return HttpResponse('Access not allowed', status=403)

    # delete bmc item
    bmc = BusinessModel.objects.get(project_id=pk, pk=request.POST.get('canvas_id'))
    bmc.delete()

    return redirect('/team-ideation-tools/business-model/projects/%s/' % str(pk))


def canvas_view(request, pk, bm):
    pk = int(pk)
    try:
        bmc = BusinessModel.objects.get(project_id=pk, pk=bm)
    except BusinessModel.DoesNotExist:
        return HttpResponse('Canvas was not found', status=404)

    project_name = ''
    for p in request.session['projects']:
        if p['pid'] == str(pk):
            project_name = p['title']

    if not project_name:
        return HttpResponse('Access not allowed', status=403)

    request.session['project_id'] = str(pk)

    return render(request, 'bm_canvas/canvas.html', {
        'bmc': bmc,
    })


def suggest_term(request, pk, bm):
    """
    :param request: The request of the user
    :param pk: The project primary key
    :return: List of suggestions
    """
    def serialize_persona(p):
        return {
            'id': p.pk,
            'name': p.name,
            'description': p.description,
            'icon': p.get_avatar_url(),
            'type': 'Persona',
            'public': p.is_public,
        }

    results = []
    for p in Persona.objects.filter(project_id=pk):
        results.append(serialize_persona(p))

    for p in Persona.objects.filter(is_public=True).exclude(project_id=pk):
        results.append(serialize_persona(p))

    return JsonResponse(data=results, safe=False)


def add_entry(request, pk, bm):
    pk = int(pk)
    if request.method != 'POST':
        return HttpResponse('Only POST requests allowed', status=400)

    bmc = BusinessModel.objects.get(project_id=pk, pk=bm)

    text = request.POST.get('text', '')
    if not text:
        return HttpResponse('`text` field is required', status=400)

    section = request.POST.get('section', '')
    if section not in [s[0] for s in BUSINESS_MODEL_SECTIONS]:
        return HttpResponse('Invalid section "%s"' % section, status=400)

    order = request.POST.get('order', '')
    if not order:
        return HttpResponse('`order` field is required', status=400)

    group_color = request.POST.get('groupColor', '#FFFFFF')

    # create the entry
    entry = BusinessModelEntry.objects.create(business_model=bmc, author=request.session['username'],
                                              section=section, text=text, order=order, group_color=group_color)

    # return the rendered entry
    return render(request, 'bm_canvas/entry.html', {'entry': entry})


def view_entry(request, pk):
    pk = int(pk)
    if request.method != 'GET':
        return HttpResponse('Only GET requests allowed', status=400)

    try:
        entry = BusinessModelEntry.objects.get(pk=pk)
    except BusinessModelEntry.DoesNotExits:
        return HttpResponse('Entry #%d was not found' % pk, status=404)

    if not entry.can_access(request):
        return HttpResponse('Access to entry #%d is forbidden' % pk, status=403)

    return render(request, 'bm_canvas/entry.html', {'entry': entry})


def update_entry_orders(request):
    if request.method != 'POST':
        return HttpResponse('Only POST requests allowed', status=400)

    # update all orders
    data = json.loads(request.POST.get('data', '[]'))
    with transaction.atomic():
        for entry in data:
            BusinessModelEntry.objects.filter(pk=entry['id']).update(order=entry['order'])

    return HttpResponse('')


def update_entry(request, pk):
    pk = int(pk)
    if request.method != 'POST':
        return HttpResponse('Only POST requests allowed', status=400)

    try:
        entry = BusinessModelEntry.objects.get(pk=pk)
    except BusinessModelEntry.DoesNotExits:
        return HttpResponse('Entry #%d was not found' % pk, status=404)

    if not entry.can_update(request):
        return HttpResponse('Access to entry #%d is forbidden' % pk, status=403)

    text = request.POST.get('text', '')
    if not text:
        return HttpResponse('`text` field is required', status=400)

    group_color = request.POST.get('groupColor', entry.group_color)

    # update & respond
    entry.text = text
    entry.group_color = group_color
    entry.save()
    return render(request, 'bm_canvas/entry.html', {'entry': entry})


def remove_entry(request, pk):
    pk = int(pk)
    if request.method != 'POST':
        return HttpResponse('Only POST requests allowed', status=400)

    try:
        entry = BusinessModelEntry.objects.get(pk=pk)
    except BusinessModelEntry.DoesNotExits:
        return HttpResponse('Entry #%d was not found' % pk, status=404)

    if not entry.can_update(request):
        return HttpResponse('Access to entry #%d is forbidden' % pk, status=403)

    # delete & respond
    entry.delete()
    return HttpResponse('Entry #%d deleted' % pk, status=204)


