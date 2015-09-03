from functools import partial, wraps
import json
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from anonymizer.datasource.connections import ConnectionManager
from forms import ConnectionConfigurationForm, Sqlite3ConnectionForm, MySQLConnectionForm, UserTableSelectionForm, \
    ColumnForm, ConnectionConfigurationManualForm
from models import ConnectionConfiguration


def get_current_configuration():
    """
    Get the current connection
    """
    qs = ConnectionConfiguration.objects.all()
    if not qs:
        return None

    return qs[len(qs) - 1]


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
        return get_current_configuration().update_info_url()


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


def suggest_users_table(request, pk):
    """
    Suggest to the user which table(s) probably contain the user info, let them select one
    """
    params = {}
    status = 200

    config = get_object_or_404(ConnectionConfiguration, pk=pk)
    manager = ConnectionManager(config.info_to_json())
    connection = manager.get(config.name)

    if request.method == 'GET':
        params['form'] = UserTableSelectionForm(connection)
    elif request.method == 'POST':
        form = UserTableSelectionForm(connection, request.POST)
        if form.is_valid():
            config.users_table = form.cleaned_data['users_table']
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
    manager = ConnectionManager(config.info_to_json())
    connection = manager.get(config.name)

    if request.method == 'GET':
        # gather suggestions
        initial = []
        columns = connection.get_data_properties(config.users_table, from_related=True)
        for column in columns:
            # auto-create property name
            from_table = column[2].split('.')[0]
            if from_table.lower() == config.users_table.lower():
                name = column[0]
            else:
                name = from_table + '_' + column[0]

            # set initial form data
            initial.append({
                'name': name,
                'c_type': column[1],
                'source': column[2],
            })

        # create formset
        ColumnFormset = formset_factory(wraps(ColumnForm)(partial(ColumnForm, all_properties=columns)), extra=0)
        formset = ColumnFormset(initial=initial)

        params['formset'] = formset
    else:
        columns = connection.get_data_properties(config.users_table, from_related=True)
        ColumnFormset = formset_factory(wraps(ColumnForm)(partial(ColumnForm, all_properties=columns)))

        formset = ColumnFormset(request.POST)
        if formset.is_valid():
            properties = []
            for form in formset:
                if form.cleaned_data['include']:  # ignore forms with include=False
                    p = {
                        'name': form.cleaned_data['name'],
                        'type': form.cleaned_data['c_type'],
                        'source': form.cleaned_data['source'],
                    }
                    if form.cleaned_data['aggregate']:
                        p['aggregate'] = form.cleaned_data['aggregate']

                    properties.append(p)

            # update configuration object
            config.properties = json.dumps(properties)
            config.total = config.create_json(user_pk_source=connection.primary_key_of(config.users_table),
                                              properties=properties)
            config.save()

            return redirect('/anonymizer/connection/%d/edit/' % config.pk)
        else:
            status = 400
            params['formset'] = formset

    return render(request, 'anonymizer/connection/select_columns.html', params, status=status)


class ConnectionConfigurationManualUpdateView(UpdateView):
    """
    Allows the manual update of the created json configuration
    """
    model = ConnectionConfiguration
    form_class = ConnectionConfigurationManualForm
    template_name = 'anonymizer/connection/update_manual.html'
    success_url = '/anonymizer/'

update_configuration = ConnectionConfigurationManualUpdateView.as_view()
