from django import forms
from django.utils.safestring import mark_safe

from ct_anonymizer.settings import MIN_USERS_IN_PERSONA
from persona_builder.models import Persona

__author__ = 'dipap'


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ['owner', 'project_id', 'campaign_id', 'query', 'based_on', ]

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].label = mark_safe('<i class="fa fa-upload"></i> Choose an avatar')
        self.fields['avatar'].widget.attrs['accept'] = 'image/*'
        self.fields['avatar'].label_suffix = ''

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # fix issue 219
        if name.strip() == '':
            self.add_error('name', 'The persona\'s name can\'t be empty')

        return name


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
        except Exception as e:
            self.add_error('query', str(e))

        return self.cleaned_data
