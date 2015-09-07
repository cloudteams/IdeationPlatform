from django import forms
from persona_builder.models import Persona

__author__ = 'dipap'


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ['owner', ]
