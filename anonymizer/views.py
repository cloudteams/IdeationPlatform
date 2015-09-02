from functools import partial, wraps
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from anonymizer.datasource.connections import ConnectionManager
from forms import ConnectionConfigurationForm, Sqlite3ConnectionForm, MySQLConnectionForm, UserTableSelectionForm, \
    ColumnForm
from models import ConnectionConfiguration


def get_current_configuration():
    """
    Get the current connection
    """
    qs = ConnectionConfiguration.objects.all()
    if not qs:
        return None

    return qs[0]


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
            initial.append({
                'name': column[0],
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
            import pdb;pdb.set_trace()
        else:
            status = 400
            params['formset'] = formset

    return render(request, 'anonymizer/connection/select_columns.html', params, status=status)
