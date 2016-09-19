from django.db.models import *

from persona_builder.models import Persona
from stories.lists import *


class Project(Model):
    project_id = IntegerField(unique=True, primary_key=True)
    project_name = CharField(max_length=1023)

    def get_absolute_url(self):
        return '/stories/projects/%d/' % self.project_id


class Scenario(Model):
    # meta info
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    project = ForeignKey(Project, related_name='project_scenarios')
    owner = TextField()

    # generic info
    project_scenario_id = SmallIntegerField()
    title = TextField()

    # the scenario itself
    description = TextField()
    tags = TextField(blank=True)
    comments = TextField(blank=True)

    def get_absolute_url(self):
        return '/stories/projects/%d/scenarios/%d/' % (self.project_id, self.pk)


class Story(Model):
    # meta info
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    project = ForeignKey(Project, related_name='project_stories')
    persona = ForeignKey(Persona)
    owner = TextField()

    # generic info
    project_story_id = SmallIntegerField()
    title = TextField()
    story_type = CharField(max_length=16, choices=STORY_TYPES)

    # the story itself
    role = TextField()
    purpose = TextField()
    target = TextField()
    acceptance_criteria = TextField(blank=True)
    comments = TextField(blank=True)

    # management
    priority = SmallIntegerField()
    estimate = SmallIntegerField()  # number of days
    state = CharField(max_length=16, choices=STORY_STATES)

    # relationships
    scenarios = ManyToManyField(Scenario, related_name='stories')
