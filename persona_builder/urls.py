from django.conf.urls import url
from persona_builder import views

__author__ = 'dipap'


urlpatterns = [
    # create new persona
    url(r'^personas/create/$', views.create_persona),

    # edit persona properties
    url(r'^personas/(?P<pk>\d+)/edit-properties/$', views.edit_persona_properties),
    url(r'^personas/(?P<pk>\d+)/$', views.view_persona),

    # list all personas
    url(r'^personas/$', views.list_personas)
]
