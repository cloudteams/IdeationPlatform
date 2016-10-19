import uuid

import datetime
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from anonymizer.models import ConnectionConfiguration
from ct_anonymizer.settings import DEBUG
from pb_oauth.xmlrpc_oauth import get_srv_instance
from persona_builder.forms import PersonaForm, PersonaPropertiesForm
from persona_builder.models import Persona, PersonaUsers
import simplejson as json


def get_active_configuration():
    """
    :return: The anonymization configuration that is currently activated
    """
    return ConnectionConfiguration.objects.get(is_active=True)


def request_context(request):
    """
    Retrieve information from request about the current context
    (username, project, campaign)
    """
    # Username
    username = request.session['username']

    # Project ID
    pid = request.session.get('project_id', '')
    if pid:
        pid = int(pid)
    else:
        pid = None

    # Campaign ID
    cid = request.session.get('campaign_id', '')
    if cid:
        cid = int(cid)
    else:
        cid = None

    return username, pid, cid


class PersonaCreateView(CreateView):
    """
    Create a new persona
    Only general information here
    """
    model = Persona
    form_class = PersonaForm
    template_name = 'persona_builder/persona/details.html'

    def form_valid(self, form):
        instance = form.save()

        # set user & project
        instance.owner, instance.project_id, instance.campaign_id = request_context(self.request)

        # create persona
        instance.save()

        return HttpResponse(instance.get_edit_properties_url() + '?initial=true')

    def get_context_data(self, **kwargs):
        context = super(PersonaCreateView, self).get_context_data(**kwargs)
        context['page'] = 'edit-info'

        return context

create_persona = PersonaCreateView.as_view()


def edit_persona_info(request, pk):
    """
    Update the basic info of a persona
    For updating the `query` of the persona see the `edit_persona_properties(request, pk)` method below
    """
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        # update persona, send info & redirect
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            persona = form.save()
            return redirect('/team-ideation-tools/propagate/?send_persona=%d&next=properties' % persona.pk)
    else:
        form = PersonaForm(instance=persona)

    ctx = {
        'form': form,
        'persona': persona,
        'page': 'edit-info',
    }

    return render(request, 'persona_builder/persona/details.html', ctx)


def edit_persona_properties(request, pk):
    """
    :param request: The request object
    :param pk: The primary key of the persona
    :return: Updates the query of the edited persona
    """
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
            if persona.update_users(user_manager, async=True):

                # save changes & show full persona view
                persona.is_ready = True
                persona.save()

                # send info to customer platform
                if DEBUG:
                    return redirect(persona.get_absolute_url())
                else:
                    return redirect('/team-ideation-tools/propagate/?send_persona=%d&next=absolute' % persona.pk)
            else:
                # not enough users
                form.add_error(None, 'Use less strict filters')

        status = 400

    params = {
        'persona': persona,
        'form': form,
        'filters': user_manager.list_filters(),
        'not_container': True,
        'show_basic_info': not request.GET.get('initial'),
        'page': 'edit-properties'
    }

    return render(request, 'persona_builder/persona/details.html', params, status=status)


def update_users(request, pk):
    """
    :param request: The request object
    :param pk: The primary key of the persona
    :return: Refreshes which of the CloudTeams users belong to this persona.
    Maintains anonymized info for users that don't change
    """
    t = datetime.datetime.now()
    persona = get_object_or_404(Persona, pk=pk)
    t2 = datetime.datetime.now(); print 'Getting persona: ' + str(t2 - t); t = t2
    config = get_active_configuration()
    user_manager = config.get_user_manager(token=persona.uuid)

    if request.method == 'POST':
        persona.update_users(user_manager, async=True)
        t = datetime.datetime.now()
        persona.save()
        t2 = datetime.datetime.now(); print 'Saving: ' + str(t2 - t); t = t2
        return redirect(persona.get_absolute_url())
    else:
        return HttpResponse('%s method not allowed' % request.method, status=400)


def propagate_persona_placeholder(request):
    # should never reach due to middleware
    return None


class PersonaDetailView(DetailView):
    """
    The details page of each persona
    """
    model = Persona
    template_name = 'persona_builder/persona/details.html'
    context_object_name = 'persona'

    def get_context_data(self, **kwargs):
        context = super(PersonaDetailView, self).get_context_data(**kwargs)
        config = get_active_configuration()
        user_manager = config.get_user_manager(token=context['persona'].uuid)

        context['properties'] = user_manager.list_filters()
        context['users'] = PersonaUsers.objects.filter(persona=context['persona'])
        context['page'] = 'stats'
        context['not_container'] = True

        return context

view_persona = PersonaDetailView.as_view()


def get_persona_users(request, pk):
    context = {
        'persona': Persona.objects.get(pk=pk),
    }

    config = get_active_configuration()
    user_manager = config.get_user_manager(token=context['persona'].uuid)

    context['properties'] = user_manager.list_filters()
    context['users'] = PersonaUsers.objects.filter(persona=context['persona'])
    context['not_container'] = True

    if not context['users'].exists():
        return HttpResponse('')
    else:
        return render(request, 'persona_builder/persona/users.html', context)


class PersonaListView(ListView):
    """
    A list of personas in the Persona Builder for this user, project & campaign
    """
    model = Persona
    template_name = 'persona_builder/persona/list.html'
    context_object_name = 'personas'

    def get_context_data(self, **kwargs):
        ctx = super(PersonaListView, self).get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx

    def get_queryset(self):
        qs = super(PersonaListView, self).get_queryset()

        if 'campaign_id' in self.request.session:
            qs = qs.filter(campaign_id=self.request.session['campaign_id'])
        elif 'project_id' in self.request.session:
            qs = qs.filter(project_id=self.request.session['project_id'])
        else:
            qs = qs.filter(is_ready=True).filter(owner=self.request.session['username'])

        # possible query
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        return qs.exclude(owner='SYSTEM')

list_personas = PersonaListView.as_view()


class PersonaPublicListView(ListView):
    """
    Public personas in the Persona Pool
    """
    model = Persona
    template_name = 'persona_builder/persona/pool.html'
    context_object_name = 'personas'

    def get_queryset(self):
        qs = super(PersonaPublicListView, self).get_queryset()
        # only public, complete personas
        qs = qs.filter(is_ready=True, is_public=True)
        return qs.exclude(owner='SYSTEM')

pool = PersonaPublicListView.as_view()


def delete_persona(request, pk):
    """
    A page that allows deleting a persona
    """
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'GET':
        return render(request, 'persona_builder/persona/delete.html', {
            'persona': persona,
            'not_container': True,
        })
    elif request.method == 'POST':
        # notify Team Platform
        return redirect('/team-ideation-tools/propagate/?send_persona=%d&delete=true' % persona.pk)
    else:
        return HttpResponse('Invalid method', status=400)


def perform_pending_action(request):
    persona_id = request.session['send_persona']
    persona = Persona.objects.get(pk=persona_id)
    srv = get_srv_instance(request.session['username'])
    persona.send_campaign_personas(srv, 'delete_persona' in request.session)
    del request.session['send_persona']

    # should the persona be deleted?
    if 'delete_persona' in request.session:
        del request.session['delete_persona']
        persona.delete()
        return redirect('/team-ideation-tools/personas/')

    # is the next page specified?
    if 'next_page' in request.session:
        nxt = request.session['next_page']
        del request.session['next_page']
        if nxt == 'absolute':
            return redirect(persona.get_absolute_url())
        elif nxt == 'properties':
            return redirect(persona.get_edit_properties_url())

    # default next page
    return redirect('/team-ideation-tools/personas/' + persona_id + '/')


def add_from_pool(request, pk):
    """
    :param request: A request object
    :param pk: The ID of the persona that should be cloned
    :return: The ID of the new persona
    """
    if request.method != 'POST':
        return HttpResponse('Only POST allowed', status=400)

    try:
        persona = Persona.objects.get(pk=pk)
    except Persona.DoesNotExist:
        return HttpResponse('Persona with id #%d not found' % pk, status=404)

    if not persona.is_public:
        return HttpResponse('Can\'t clone private personas', status=403)

    # clone the persona with the appropriate properties
    new_persona = persona
    new_persona.pk = None
    new_persona.uuid = uuid.uuid4()
    new_persona.owner, new_persona.project_id, new_persona.campaign_id = request_context(request)
    new_persona.based_on_id = pk
    new_persona.save()

    # clone persona users
    with transaction.atomic():
        for pu in PersonaUsers.objects.filter(persona_id=pk):
            new_pu = pu
            new_pu.pk = None
            new_pu.persona_id = new_persona.pk
            new_pu.save()

    return HttpResponse('%d' % new_persona.pk)
