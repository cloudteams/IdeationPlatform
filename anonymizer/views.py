from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from forms import ConnectionConfigurationForm, Sqlite3ConnectionForm
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

    if request.method == 'GET':
        params['form'] = Sqlite3ConnectionForm()
    elif request.method == 'POST':
        form = Sqlite3ConnectionForm(request)
        import pdb;pdb.set_trace()

    return render(request, 'anonymizer/connection/update_info.html', params)
