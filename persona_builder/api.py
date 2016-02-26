import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson as json

from anonymizer.models import ConnectionConfiguration
from ct_anonymizer.settings import MEDIA_URL
from persona_builder.forms import PersonaAPIForm, PersonaPropertiesForm
from persona_builder.models import Persona, PersonaUsers
from persona_builder.views import get_active_configuration

__author__ = 'dipap'


def info(request):
    """
    Returns information about the properties supported in the creation of the persona
    """
    if request.method == 'GET':
        config = get_active_configuration()
        return JsonResponse(config.get_user_manager().list_filters(ignore_options=True), safe=False)
    else:
        return JsonResponse({'error': 'Only GET method allowed'}, status=400)


def http_address(host):
    return 'http://%s' % host.META['HTTP_HOST']


def get_persona_data(request, persona):
    p_info = {
        'id': str(persona.pk),
        # 'uuid': str(persona.uuid),
        'owner': persona.owner,
        'name': persona.name,
        'description': persona.description,
        'query': persona.query,
        'user': json.loads(persona.users),
        'is_public': persona.is_public,
    }

    if persona.avatar:
        p_info['avatar'] = http_address(request) + MEDIA_URL + persona.avatar.name
    else:
        p_info['avatar'] = None

    return p_info


def update_query(p, data):
    if 'query' in data:
        # set query
        config = get_active_configuration()
        user_manager = config.get_user_manager(token=p.uuid)
        p_form = PersonaPropertiesForm(user_manager, data)
        if not p_form.is_valid():
            return JsonResponse({'error': p_form.errors}, status=400, safe=False)

        p.uuid = uuid.uuid4()
        user_manager.reset_token(p.uuid)
        p.query = p_form.cleaned_data['query']

        # generate users according to query
        p.update_users(user_manager)

    # save changes & show full persona view
    p.is_ready = True
    p.save()


@csrf_exempt
# our API calls are csrf_exempt because other authorization techniques
# will be used to ensure communication with BSCW
def personas(request):
    """
    Actions over the personas list
    """
    if request.method == 'GET':  # list of exiting personas
        sqs = Persona.objects.filter(is_ready=True)
        if 'public' in request.GET:
            sqs = sqs.filter(is_public=True)

        result = [get_persona_data(request, persona) for persona in sqs]
        return JsonResponse(result, safe=False)
    elif request.method == 'POST':  # create a new persona
        form = PersonaAPIForm(request.POST)

        if not form.is_valid():
            return JsonResponse({'error': form.errors}, status=400, safe=False)

        # create the (not ready) object
        p = form.save()

        err = update_query(p, request.POST)
        if err:  # some error occurred
            return err

        return JsonResponse(get_persona_data(request, p), safe=False, status=201)
    elif request.method in ['PUT', 'DELETE']:
        return JsonResponse({'error': '%s method over entire persona list disabled' % request.method}, status=400)
    else:
        return JsonResponse({'error': 'Only GET, POST methods allowed'}, status=400)


@csrf_exempt
def persona(request, pk):
    """
    Actions over a specific persona
    """
    try:
        p = Persona.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Persona #%s not found' % pk}, status=404)

    if request.method == 'GET':
        return JsonResponse(get_persona_data(request, p), safe=False)
    elif request.method == 'POST':
        data = request.POST.copy()
        # (partial) update
        if 'name' not in data:
            data['name'] = p.name
        if 'description' not in data:
            data['description'] = p.description
        if 'avatar' not in data:
            data['avatar'] = p.avatar
        if 'is_public' not in data:
            data['is_public'] = p.is_public

        # validate form
        form = PersonaAPIForm(data, instance=p)

        if not form.is_valid():
            return JsonResponse({'error': form.errors}, status=400)

        # special case for query -- additional actions required
        if 'query' in data and p.query != data.get('query'):
            err = update_query(p, data)
            if err:  # some error occurred
                return err

        return JsonResponse(get_persona_data(request, p), safe=False)
    elif request.method == 'DELETE':
        p.delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({'error': 'Only GET, POST, DELETE methods allowed'}, status=400)


@csrf_exempt
def create_default_persona(request):
    """
    :param request: Must contain the new persona
    :return: HTTP 201 if the system persona was created, HTTP 204 if it already existed
    """
    if request.method != 'POST':
        return HttpResponse('Only POST method allowed', status=400)

    # get the project id
    pid = request.POST.get('project')
    if not pid:
        return HttpResponse('`project` field is required', status=400)

    try:
        pid = int(pid)
    except ValueError:
        return HttpResponse('`project` must be the project ID ("%s" is not an int)' % pid, status=400)

    # check if the persona already exists
    if Persona.objects.filter(project_id=pid, owner='SYSTEM').exists():
        return HttpResponse('', status=204)

    # create the system persona
    p = Persona.objects.create(project_id=pid, owner='SYSTEM', query='',
                               description='Generic project persona', is_ready=True, is_public=False)

    # find the users
    p.update_users(ConnectionConfiguration.objects.get(is_active=True).get_user_manager())
    return HttpResponse('', status=201)


def find_user(request):
    """
    :param request: Must contain actual user pk and the project pk in request GET
    :return: The anonymized user info from the first persona where user was found
    """
    if request.method != 'GET':
        return HttpResponse('Only GET method allowed', status=400)

    # get user & project id
    uid = request.GET.get('user')
    if not uid:
        return HttpResponse('`user` field is required', status=400)

    try:
        uid = int(uid)
    except ValueError:
        return HttpResponse('`user` must be the user ID ("%s" not an int)' % uid, status=400)

    pid = request.GET.get('project')
    if not pid:
        return HttpResponse('`project` field is required', status=400)

    try:
        pid = int(pid)
    except ValueError:
        return HttpResponse('`project` must be the project ID ("%s" is not an int)' % pid, status=400)

    res = PersonaUsers.objects.filter(user_id=uid, persona__project_id=pid).exclude(persona__owner='SYSTEM')
    if not res:
        res = PersonaUsers.objects.filter(user_id=uid, persona__project_id=pid, persona__owner='SYSTEM')

    p = res[0].persona
    users = json.loads(p.users)
    for user in users:
        if user['__id__'] == uid:
            result = user
            result.pop('__id__')
            result['persona'] = p.pk

            return JsonResponse(result, safe=False)

