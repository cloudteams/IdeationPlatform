from django.forms import *
from django.utils.safestring import mark_safe

from stories.models import *

__author__ = 'dipap'


class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        exclude = ['created', 'updated', 'project', 'owner', 'project_scenario_id', ]
        widgets = {
            'title': TextInput(),
            'tags': TextInput(attrs={'placeholder': 'Separate different tags by spaces'}),
        }


class StoryForm(ModelForm):
    class Meta:
        model = Story
        exclude = ['created', 'updated', 'project', 'owner', 'project_story_id', 'scenarios']
        widgets = {
            'title': TextInput(),
            'story_type': RadioSelect(),

            'role': Textarea(attrs={'rows': 2, 'cols': 15}),
            'purpose': Textarea(attrs={'rows': 4, 'cols': 15}),
            'target': Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        # get the project ID for filtering personas
        project_id = kwargs.pop('project_id')

        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['persona'].label = 'Related persona'
        self.fields['story_type'].label = 'Type'

        self.fields['role'].label = 'As a'
        self.fields['purpose'].label = 'I want to'
        self.fields['target'].label = 'so that'

        self.fields['estimate'].label = 'Estimate (# days)'

        # filter possible personas
        self.fields['persona'].queryset = Persona.objects.filter(is_ready=True).filter(Q(is_public=True) |
                                                                                       Q(project_id=project_id))
