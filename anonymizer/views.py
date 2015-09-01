from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from forms import ConnectionConfigurationForm
from models import ConnectionConfiguration


class ConnectionConfigurationCreateView(CreateView):
    model = ConnectionConfiguration
    form_class = ConnectionConfigurationForm
    template_name = 'anonymizer/connection/create.html'

    def dispatch(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
