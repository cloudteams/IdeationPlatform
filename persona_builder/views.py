import uuid
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from anonymizer.models import ConnectionConfiguration
from persona_builder.forms import PersonaForm, PersonaPropertiesForm
from persona_builder.models import Persona
import simplejson as json


def get_active_configuration():
    return ConnectionConfiguration.objects.get(is_active=True)


class PersonaCreateView(CreateView):
    """
    Create a new persona
    Only general information here
    """
    model = Persona
    form_class = PersonaForm
    template_name = 'persona_builder/persona/create.html'

    def get_success_url(self):
        return self.object.get_edit_properties_url()

create_persona = PersonaCreateView.as_view()


def edit_persona_properties(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    config = get_active_configuration()
    user_manager = config.get_user_manager(token=persona.uuid)

    status = 200

    if request.method == 'GET':
        # user_manager is not necessary for getting the form, just when validating
        form = PersonaPropertiesForm(None, initial={'query': persona.query})

    elif request.method == 'POST':
        form = PersonaPropertiesForm(user_manager, request.POST)
        if form.is_valid():
            # if the query changes, we have to update the UUID of the persona
            if persona.query != form.cleaned_data['query']:
                persona.uuid = uuid.uuid4()
                user_manager.reset_token(persona.uuid)
                persona.query = form.cleaned_data['query']

            # generate users according to query
            persona.update_users(user_manager)

            # save changes & show full persona view
            persona.is_ready = True
            persona.save()

            # send info to customer platform
            return redirect(persona.get_absolute_url())
        else:
            status = 400

    params = {
        'persona': persona,
        'form': form,
        'filters': user_manager.list_filters(),
    }

    return render(request, 'persona_builder/persona/edit_properties.html', params, status=status)


def update_users(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    config = get_active_configuration()
    user_manager = config.get_user_manager(token=persona.uuid)

    if request.method == 'POST':
        persona.update_users(user_manager)
        persona.save()
        return redirect(persona.get_absolute_url())
    else:
        return HttpResponse('%s method not allowed' % request.method, status=400)


class PersonaDetailView(DetailView):
    model = Persona
    template_name = 'persona_builder/persona/details.html'
    context_object_name = 'persona'

    def get_context_data(self, **kwargs):
        context = super(PersonaDetailView, self).get_context_data(**kwargs)
        config = get_active_configuration()
        user_manager = config.get_user_manager(token=context['persona'].uuid)

        context['properties'] = user_manager.list_filters()
        context['users'] = json.loads(kwargs['object'].users)

        return context

view_persona = PersonaDetailView.as_view()


class PersonaListView(ListView):
    model = Persona
    template_name = 'persona_builder/persona/list.html'
    context_object_name = 'personas'

    def get_queryset(self):
        return super(PersonaListView, self).get_queryset().filter(is_ready=True)

list_personas = PersonaListView.as_view()


class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'persona_builder/persona/delete.html'
    context_object_name = 'persona'
    success_url = '/persona-builder/personas/'


delete_persona = PersonaDeleteView.as_view()
