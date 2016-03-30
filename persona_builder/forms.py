from django import forms

from ct_anonymizer.settings import MIN_USERS_IN_PERSONA
from persona_builder.models import Persona

__author__ = 'dipap'


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ['owner', 'project_id', 'campaign_id', 'query', ]


class PersonaAPIForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = []


class PersonaPropertiesForm(forms.Form):
    query = forms.CharField(required=False)

    def __init__(self, user_manager, *args, **kwargs):
        super(PersonaPropertiesForm, self).__init__(*args, **kwargs)
        self.user_manager = user_manager

    def clean(self):
        # default validation
        super(PersonaPropertiesForm, self).clean()

        try:
            # check number of users in persona
            if 'query' in self.cleaned_data:
                q = self.cleaned_data['query']
            else:
                q = ''
            if self.user_manager.count(q) < MIN_USERS_IN_PERSONA:
                self.add_error(None, 'Use less strict filters')
        except Exception as e:
            self.add_error('query', str(e))

        return self.cleaned_data
