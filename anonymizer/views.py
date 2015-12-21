from functools import partial, wraps
import json
import datetime
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView
import simplejson
from anonymizer.lists import PROVIDER_PLUGINS
from forms import ConnectionConfigurationForm, Sqlite3ConnectionForm, MySQLConnectionForm, UserTableSelectionForm, \
    ColumnForm, validate_unique_across, PostgresConnectionForm
from models import ConnectionConfiguration

# patch simplejson library to serialize datetimes
simplejson.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)


def home(request):
    params = {
        'configurations': ConnectionConfiguration.objects.all(),
    }

    return render(request, 'anonymizer/connection/home.html', params)


class ConnectionConfigurationCreateView(CreateView):
    """
    Allows the creation of the connection's configuration
    """
    model = ConnectionConfiguration
    form_class = ConnectionConfigurationForm
    template_name = 'anonymizer/connection/create.html'

    def get_success_url(self):
        return self.object.update_info_url()


create_configuration = ConnectionConfigurationCreateView.as_view()


def sqlite3_info(request, pk):
    """
    Update the info of a connection to an sqlite3 database
    """
    params = {}
    status = 200

    if request.method == 'GET':
        params['form'] = Sqlite3ConnectionForm()
    elif request.method == 'POST':
        form = Sqlite3ConnectionForm(request.POST, request.FILES)
        if form.is_valid():
            config = get_object_or_404(ConnectionConfiguration, pk=pk)
            config.info = '''
                  "name": "''' + form.cleaned_data['path'] + '''"
            '''
            config.save()

            return redirect('/anonymizer/connection/%d/suggest-user-table/' % config.pk)
        else:
            status = 400
            params['form'] = form

    return render(request, 'anonymizer/connection/update_info.html', params, status=status)


def mysql_info(request, pk):
    """
    Update the info of a connection to a mysql database
    """
    params = {}
    status = 200

    if request.method == 'GET':
        params['form'] = MySQLConnectionForm()
    elif request.method == 'POST':
        form = MySQLConnectionForm(request.POST)
        if form.is_valid():
            config = get_object_or_404(ConnectionConfiguration, pk=pk)
            data = form.cleaned_data
            config.info = '''
                "name": "''' + data['database'] + '''",
                "user": "''' + data['user'] + '''",
                "password": "''' + data['password'] + '''",
                "host": "''' + data['host'] + '''",
                "port": "''' + data['port'] + '''"
            '''
            config.save()

            return redirect('/anonymizer/connection/%d/suggest-user-table/' % config.pk)
        else:
            status = 400
            params['form'] = form

    return render(request, 'anonymizer/connection/update_info.html', params, status=status)


def postgres_info(request, pk):
    """
    Update the info of a connection to a postgres database
    """
    params = {}
    status = 200

    if request.method == 'GET':
        params['form'] = PostgresConnectionForm()
    elif request.method == 'POST':
        form = PostgresConnectionForm(request.POST)
        if form.is_valid():
            config = get_object_or_404(ConnectionConfiguration, pk=pk)
            data = form.cleaned_data
            config.info = '''
                "name": "''' + data['database'] + '''",
                "user": "''' + data['user'] + '''",
                "password": "''' + data['password'] + '''",
                "host": "''' + data['host'] + '''",
                "port": "''' + data['port'] + '''"
            '''
            config.save()

            return redirect('/anonymizer/connection/%d/suggest-user-table/' % config.pk)
        else:
            status = 400
            params['form'] = form

    return render(request, 'anonymizer/connection/update_info.html', params, status=status)


def suggest_users_table(request, pk):
    """
    Suggest to the user which table(s) probably contain the user info, let them select one
    """
    params = {}
    status = 200

    config = get_object_or_404(ConnectionConfiguration, pk=pk)
    connection = config.get_connection()

    if request.method == 'GET':
        params['form'] = UserTableSelectionForm(connection)
    elif request.method == 'POST':
        form = UserTableSelectionForm(connection, request.POST)
        if form.is_valid():
            config.users_table = form.cleaned_data['users_table']

            # detect primary key
            config.user_pk = connection.primary_key_of(config.users_table)

            # load default properties
            data_properties = connection.get_data_properties(config.users_table, from_related=True)
            few_properties = connection.get_data_properties(config.users_table)
            columns = few_properties[0]
            columns.insert(0, ('', '', ''))
            config.properties = config.get_default_properties(few_properties[0])
            config.foreign_keys = json.dumps(data_properties[1])

            # save changes
            config.save()

            return redirect('/anonymizer/connection/%d/select-columns/' % config.pk)
        else:
            status = 400
            params['form'] = form

    return render(request, 'anonymizer/connection/suggest_user_table.html', params, status=status)


def select_columns(request, pk):
    """
    Choose which columns to keep
    """
    params = {}
    status = 200

    config = get_object_or_404(ConnectionConfiguration, pk=pk)
    connection = config.get_connection()

    columns = connection.get_data_properties(config.users_table, from_related=True)[0]
    columns.insert(0, ('', '', ''))

    if not config.properties:
        # setup default properties
        config.properties = config.get_default_properties(columns)
        config.save()

    if request.method == 'GET':
        # gather suggestions
        initial = json.loads(config.properties)

        # resolve providers
        for initial_form in initial:
            for plugin in PROVIDER_PLUGINS:
                total_source = initial_form['source']
                if total_source.split('(')[0] != plugin['source']:
                    continue
                initial_form['source'] = total_source.split('(')[0]

                if 'args' in plugin:
                    plugin_params = total_source.split('(')[1][:-1]

                    for idx, option in enumerate(plugin_params.split(',')):
                        initial_form[plugin['source'] + '__param__' + plugin['args'][idx][0]] = option

        # create formset
        ColumnFormset = formset_factory(wraps(ColumnForm)(partial(ColumnForm, all_properties=columns)), extra=0)
        formset = ColumnFormset(initial=initial)

        params['formset'] = formset
    else:
        ColumnFormset = formset_factory(wraps(ColumnForm)(partial(ColumnForm, all_properties=columns)))
        formset = ColumnFormset(request.POST)

        if formset.is_valid():
            validate_unique_across(formset, ['name'])

        if formset.is_valid():
            properties = []
            for form in formset:
                p = {
                    'name': form.cleaned_data['name'],
                    'source': form.cleaned_data['source'],
                }

                if 'expose' in form.cleaned_data:
                    p['expose'] = bool(form.cleaned_data['expose'])
                else:
                    p['expose'] = False

                if 'options_auto' in form.cleaned_data:
                    p['options_auto'] = bool(form.cleaned_data['options_auto'])
                else:
                    p['options_auto'] = False

                if form.cleaned_data['aggregate']:
                    p['aggregate'] = form.cleaned_data['aggregate']

                if p['source'][0] != '^':  # don't try to join provider data
                    table_name = p['source'].split('.')[0]

                    # get type
                    if 'aggregate' in p and p['aggregate'] == 'avg':
                        p['type'] = 'FLOAT'
                    else:
                        for column in columns:
                            if p['source'] == column[2]:
                                p['type'] = column[1]
                                break

                    if table_name.lower() != config.users_table.lower():
                        if 'rel_to' in p:
                            rel_table = form.cleaned_data['rel_table']
                        else:
                            rel_table = config.users_table

                        p['rel_fk'] = connection.get_foreign_key_between(table_name, rel_table)
                        p['rel_to'] = connection.primary_key_of(rel_table)
                else:
                    # read plugin options
                    plugin_info = [plugin_info for plugin_info in PROVIDER_PLUGINS if
                                   plugin_info['source'] == p['source']][0]

                    # plugin return type
                    p['type'] = plugin_info['type']

                    # argument management
                    if 'args' in plugin_info:
                        plugin_options = plugin_info['args']
                        plugin_name = p['source']

                        option_values = []
                        for option in plugin_options:
                            key = plugin_name + '__param__' + option[0]
                            if key in form.cleaned_data:
                                option_values.append(form.cleaned_data[key])

                        p['source'] = '%s(%s)' % (plugin_name, ','.join(option_values))
                    else:
                        p['source'] = '%s()' % p['source']

                properties.append(p)

            # update configuration object
            config.properties = json.dumps(properties)
            config.save()

            return redirect('/anonymizer/')
        else:
            status = 400
            params['formset'] = formset

    return render(request, 'anonymizer/connection/select_columns.html', params, status=status)


def set_active(request, pk):
    """
    Changes the active configuration
    """
    if request.method == 'POST':
        target = get_object_or_404(ConnectionConfiguration, pk=pk)

        for cc in ConnectionConfiguration.objects.all():
            if cc == target:
                cc.is_active = True
            else:
                cc.is_active = False

            cc.save()

        return redirect('/anonymizer/')
    else:
        return HttpResponse('Only POST method allowed', status=400)


def query_connection(request, pk):
    """
    Execute a query against a connection
    """
    status = 200

    config = get_object_or_404(ConnectionConfiguration, pk=pk)
    user_manager = config.get_user_manager()

    if request.method != 'GET':
        return HttpResponse('Only GET requests are allowed', status=400)

    q = request.GET['q']
    result = ''

    if q:
        try:
            if q == 'all()':
                result = user_manager.all()
            elif q.startswith('filter'):
                pos = len('filter(')
                filters = q[pos:-1]

                result = user_manager.filter(filters)
            elif q.startswith('count'):
                pos = len('count(')
                filters = q[pos:-1]

                result = user_manager.count(filters)
            elif q == 'properties':
                return JsonResponse(user_manager.list_filters(), safe=False)
            elif q == 'help':
                result = """
    Commands:
        - all(): Fetch all records
        - filter(some_filter): Fetch records based on `some_filter`
        - count(some_filters): Count records based on `some_filter`
        - properties: Show all acceptable attributes

    Examples of filter usage:
        - filter(age>30)
        - filter(age<20 and run_distance>500)

    Available data properties:
"""

                for f in user_manager.list_filters():
                    result += "        %s" % f['name']
                    if f['has_options']():
                        result += ' / options: '
                        options_info = []
                        for o in f['get_options']():
                            options_info.append('%s (%s)' % (o[0], o[1]))

                        result += ','.join(options_info)

                    result += '\n'
            else:
                raise Exception('Unknown command: %s' % q)

            if q != 'help':
                result = simplejson.dumps(result, indent=4)

        except Exception as e:
            status = 400
            result = str(e)

    return HttpResponse(result, status=status)


def console(request, pk):
    params = {
        'configuration': get_object_or_404(ConnectionConfiguration, pk=pk)
    }

    return render(request, 'anonymizer/connection/test_console.html', params)


class ConnectionConfigurationManualDeleteView(DeleteView):
    model = ConnectionConfiguration
    template_name = 'anonymizer/connection/delete.html'
    context_object_name = 'configuration'
    success_url = '/anonymizer/'


delete_view = ConnectionConfigurationManualDeleteView.as_view()
