from django.conf.urls import url
from stories import views

__author__ = 'dipap'


urlpatterns = [
    # project
    url(r'^projects/(?P<project_id>[\w-]+)/$', views.project_view, name='project-stories'),

    # scenario
    url(r'^projects/(?P<project_id>[\w-]+)/add-scenario/$', views.add_scenario, name='add-scenario'),
    url(r'^projects/(?P<project_id>[\w-]+)/scenarios/(?P<scenario_id>[\w-]+)/$', views.scenario_details,
        name='scenario-details'),
]
