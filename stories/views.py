from django.http import HttpResponse
from django.shortcuts import render, redirect

from stories.models import *
from stories.forms import *


def project_view(request, project_id):
    """
    Open a project in the stories app
    """
    pk = int(project_id)
    try:
        project = Project.objects.get(project_id=pk)
    except Project.DoesNotExist:
        project_name = ''
        for p in request.session['projects']:
            if p['pid'] == str(pk):
                project_name = p['title']

        if not project_name:
            return HttpResponse('Project #%d was not found on TeamPlatform' % pk, status=404)

        project = Project.objects.create(project_id=pk, project_name=project_name)

    return render(request, 'stories/project.html', {
        'project': project,
    })


def add_scenario(request, project_id):
    """
    Create a new scenario
    """
    project_id = int(project_id)
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id)

    if request.method == 'GET':
        form = ScenarioForm()
    if request.method == 'POST':
        form = ScenarioForm(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)

            # fill in non-form fields
            scenario.owner = request.session['username']
            scenario.project = project

            # auto-generate ID
            ids = Scenario.objects.filter(project=project).aggregate(Max('project_scenario_id'))

            if ids['project_scenario_id__max'] is not None:
                scenario.project_scenario_id = int(ids['project_scenario_id__max']) + 1
            else:
                scenario.project_scenario_id = 1

            # save
            scenario.save()
            return redirect(scenario.get_absolute_url())

    ctx = {
        'project': project,
        'form': form,
    }

    return render(request, 'scenarios/create.html', ctx)


def scenario_details(request, project_id, scenario_id):
    """
    Create a new scenario
    """
    project_id = int(project_id)
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id)

    # get scenario
    scenario_id = int(scenario_id)
    try:
        scenario = Scenario.objects.get(pk=scenario_id, project_id=project_id)
    except Scenario.DoesNotExist:
        return HttpResponse('Scenario #%d does not exist' % scenario_id)

    ctx = {
        'project': project,
        'scenario': scenario,
    }

    return render(request, 'scenarios/details.html', ctx)
