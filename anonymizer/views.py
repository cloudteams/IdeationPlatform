from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from forms import ConnectionConfigurationForm, Sqlite3ConnectionForm, MySQLConnectionForm
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
                  "NAME": "''' + form.cleaned_data['path'] + '''",
            '''
            config.save()

            return redirect('/anonymizer/connection/create/')
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
            config.info = '''{
                "NAME": "''' + data['database'] + '''",
                'USER': "''' + data['user'] + '''",
                'PASSWORD': "''' + data['password'] + '''",
                'HOST': "''' + data['host'] + '''",
                'PORT': "''' + data['port'] + '''"
            '''
            config.save()

            return redirect('/anonymizer/connection/create/')
        else:
            status = 400
            params['form'] = form

    return render(request, 'anonymizer/connection/update_info.html', params, status=status)
