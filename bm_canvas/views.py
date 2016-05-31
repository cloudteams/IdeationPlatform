from django.http import HttpResponse
from django.shortcuts import render

from bm_canvas.lists import BUSINESS_MODEL_SECTIONS
from bm_canvas.models import BusinessModel, BusinessModelEntry


def project_view(request, pk):
    try:
        bmc = BusinessModel.objects.get(project_id=pk)
    except BusinessModel.DoesNotExist:
        project_name = ''
        for p in request.session['projects']:
            if p['pid'] == pk:
                project_name = p['title']

        if not project_name:
            return HttpResponse('Project #%d was not found on TeamPlatform' % pk)

        bmc = BusinessModel.objects.create(project_id=pk, project_name=project_name)

    return render(request, 'bm_canvas/canvas.html', {
        'bmc': bmc
    })


def add_entry(request, pk):
    if request.method != 'POST':
        return HttpResponse('Only POST requests allowed', status=400)

    bmc = BusinessModel.objects.get(project_id=pk)

    text = request.POST.get('text', '')
    if not text:
        return HttpResponse('`text` field is required', status=400)

    section = request.POST.get('section', '')
    if section not in [s[0] for s in BUSINESS_MODEL_SECTIONS]:
        return HttpResponse('Invalid section "%s"' % section, status=400)

    # create the entry
    entry = BusinessModelEntry.objects.create(business_model=bmc, author=request.session['username'],
                                              section=section, text=text)

    # return the rendered entry
    return render(request, 'bm_canvas/entry.html', {'entry': entry})
