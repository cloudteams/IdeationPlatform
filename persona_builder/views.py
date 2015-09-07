from django.shortcuts import render
from django.views.generic import CreateView
from persona_builder.forms import PersonaForm
from persona_builder.models import Persona


class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'persona_builder/persona/create.html'

    def get_success_url(self):
        return self.object.get_edit_properties_url()

create_persona = PersonaCreateView.as_view()


def edit_persona_properties(request, pk):
    return None
