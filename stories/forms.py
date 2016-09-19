from django.forms import *
from django.utils.safestring import mark_safe

from stories.models import *

__author__ = 'dipap'


class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        exclude = ['created', 'created', 'project', 'owner', 'project_scenario_id', ]
        widgets = {
            'title': TextInput(),
            'tags': TextInput(attrs={'placeholder': 'Separate different tags by spaces'}),
        }
