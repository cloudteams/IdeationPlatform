from django import forms
from ct_anonymizer.settings import MIN_USERS_IN_PERSONA
from persona_builder.models import Persona

__author__ = 'dipap'


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ['owner', ]


class PersonaPropertiesForm(forms.Form):
    query = forms.CharField()

    def __init__(self, user_manager, *args, **kwargs):
        super(PersonaPropertiesForm, self).__init__(*args, **kwargs)
        self.user_manager = user_manager

    def clean(self):
        # default validation
        super(PersonaPropertiesForm, self).clean()

        # check number of users in persona
        if self.user_manager.count(self.cleaned_data['query']) < MIN_USERS_IN_PERSONA:
            self.add_error(None, 'Use less strict filters')

        return self.cleaned_data
