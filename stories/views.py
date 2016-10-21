from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

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

    request.session['project_id'] = project_id

    # order scenarios
    scenarios = project.project_scenarios.all().order_by('project_scenario_id')

    scenario_order = request.GET.get('order_scenarios_by', 'scenario_id')

    if scenario_order == 'title':
        scenarios = scenarios.order_by('title')
    elif scenario_order == 'num_stories':
        scenarios = scenarios.annotate(num_stories=Count('stories')).order_by('-num_stories')
    elif scenario_order == 'num_stories':
        scenarios = scenarios.annotate(num_stories=Count('stories')).order_by('-num_stories')
    elif scenario_order == 'updated':
        scenarios = scenarios.order_by('-updated')
    elif scenario_order == 'created':
        scenarios = scenarios.order_by('-created')

    return render(request, 'stories/project.html', {
        'project': project,
        'scenarios': scenarios,
        'scenario_order': scenario_order,
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
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id, status=404)

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
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id, status=404)

    # get scenario
    scenario_id = int(scenario_id)
    try:
        scenario = Scenario.objects.get(pk=scenario_id, project_id=project_id)
    except Scenario.DoesNotExist:
        return HttpResponse('Scenario #%d does not exist' % scenario_id, status=404)

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
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id, status=404)

    # get scenario
    scenario_id = int(scenario_id)
    try:
        scenario = Scenario.objects.get(pk=scenario_id, project_id=project_id)
    except Scenario.DoesNotExist:
        return HttpResponse('Scenario #%d does not exist' % scenario_id, status=404)

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
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id, status=404)

    # optionally get scenario
    if scenario_id is not None:
        scenario_id = int(scenario_id)
        try:
            scenario = Scenario.objects.get(pk=scenario_id, project_id=project_id)
        except Scenario.DoesNotExist:
            return HttpResponse('Scenario #%d does not exist' % scenario_id, status=404)
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
        'scenario': scenario,
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
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id, status=404)

    # get story
    story_id = int(story_id)
    try:
        story = Story.objects.get(pk=story_id, project_id=project_id)
    except Story.DoesNotExist:
        return HttpResponse('Story #%d does not exist' % story_id, status=404)

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
        return HttpResponse('Project #%d was not found on TeamPlatform' % project_id, status=404)

    # get story
    story_id = int(story_id)
    try:
        story = Story.objects.get(pk=story_id, project_id=project_id)
    except Story.DoesNotExist:
        return HttpResponse('Story #%d does not exist' % story_id, status=404)

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
        'story': story,
    }

    return render(request, 'stories/edit.html', ctx)


def stories_to_add(request, scenario_id):
    """
    List all stories that can be added in the scenario
    """
    # get scenario
    scenario_id = int(scenario_id)
    try:
        scenario = Scenario.objects.get(pk=scenario_id)
    except Scenario.DoesNotExist:
        return HttpResponse('Scenario #%d does not exist' % scenario_id, status=404)

    # get all project stories that are not in the scenario
    stories = Story.objects.filter(project=scenario.project).exclude(scenarios=scenario).order_by('project_story_id')

    # render table
    return render(request, 'stories/add-table.html', {
        'scenario': scenario,
        'stories': stories,
    })


@csrf_exempt
def add_story_to_scenario(request, scenario_id):
    """
    Adds an existing story to the scenario
    """
    if request.method != 'POST':
        return HttpResponse('Invalid method - only POST allowed', status=400)

    # get scenario
    scenario_id = int(scenario_id)
    try:
        scenario = Scenario.objects.get(pk=scenario_id)
    except Scenario.DoesNotExist:
        return HttpResponse('Scenario #%d does not exist' % scenario_id, status=404)

    # get story
    story_id = request.POST.get('story_id', '')
    if not story_id:
        return HttpResponse('`story_id` must be provided', status=400)

    story_id = int(story_id)
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return HttpResponse('Story #%d does not exist' % story_id)

    # check if story can be added
    ids = Story.objects.filter(project=scenario.project).exclude(scenarios=scenario).values_list('pk', flat=True)
    if story_id not in ids:
        return HttpResponse('Story #%d could not be added to scenario' % story_id, status=400)

    # add story to scenario
    story.scenarios.add(scenario)
    story.save()

    # return OK response
    return HttpResponse('')
