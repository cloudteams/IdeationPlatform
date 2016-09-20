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

"""
Scenario
"""


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
    Scenario details page
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


def edit_scenario(request, project_id, scenario_id):
    """
    Update an existing scenario
    """
    project_id = int(project_id)
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id)

    # get story
    scenario_id = int(scenario_id)
    try:
        scenario = Scenario.objects.get(pk=scenario_id, project_id=project_id)
    except Scenario.DoesNotExist:
        return HttpResponse('Scenario #%d does not exist' % scenario_id)

    if request.method == 'GET':
        form = ScenarioForm(instance=scenario)
    if request.method == 'POST':
        form = ScenarioForm(request.POST, instance=scenario)
        if form.is_valid():
            scenario = form.save(commit=False)

            # save
            scenario.save()

            # redirect to story
            return redirect(scenario.get_absolute_url())

    ctx = {
        'project': project,
        'form': form,
    }

    return render(request, 'scenarios/edit.html', ctx)

"""
Story
"""


def add_story(request, project_id, scenario_id=None):
    """
    Create a new story
    """
    project_id = int(project_id)
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id)

    # optionally get scenario
    if scenario_id is not None:
        scenario_id = int(scenario_id)
        try:
            scenario = Scenario.objects.get(pk=scenario_id, project_id=project_id)
        except Scenario.DoesNotExist:
            return HttpResponse('Scenario #%d does not exist' % scenario_id)
    else:
        scenario = None

    if request.method == 'GET':
        form = StoryForm(project_id=project_id)
    if request.method == 'POST':
        form = StoryForm(request.POST, project_id=project_id)
        if form.is_valid():
            story = form.save(commit=False)

            # fill in non-form fields
            story.owner = request.session['username']
            story.project = project

            # auto-generate ID
            ids = Story.objects.filter(project=project).aggregate(Max('project_story_id'))

            if ids['project_story_id__max'] is not None:
                story.project_story_id = int(ids['project_story_id__max']) + 1
            else:
                story.project_story_id = 1

            # save
            story.save()

            # add default scenario
            story.scenarios.add(scenario)

            # redirect to story
            return redirect(story.get_absolute_url())

    ctx = {
        'project': project,
        'form': form,
    }

    return render(request, 'stories/create.html', ctx)


def story_details(request, project_id, story_id):
    """
    Story details page
    """
    project_id = int(project_id)
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id)

    # get story
    story_id = int(story_id)
    try:
        story = Story.objects.get(pk=story_id, project_id=project_id)
    except Story.DoesNotExist:
        return HttpResponse('Story #%d does not exist' % story_id)

    # find related stories
    related_stories = []
    for sc in story.scenarios.all():
        for st in sc.stories.all().exclude(pk=story.pk):
            related_stories.append(st)

    ctx = {
        'project': project,
        'story': story,
        'related_stories': related_stories,
    }

    return render(request, 'stories/details.html', ctx)


def edit_story(request, project_id, story_id):
    """
    Update an existing story
    """
    project_id = int(project_id)
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id)

    # get story
    story_id = int(story_id)
    try:
        story = Story.objects.get(pk=story_id, project_id=project_id)
    except Story.DoesNotExist:
        return HttpResponse('Story #%d does not exist' % story_id)

    if request.method == 'GET':
        form = StoryForm(instance=story, project_id=project_id)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story, project_id=project_id)
        if form.is_valid():
            story = form.save(commit=False)

            # save
            story.save()

            # redirect to story
            return redirect(story.get_absolute_url())

    ctx = {
        'project': project,
        'form': form,
    }

    return render(request, 'stories/edit.html', ctx)
