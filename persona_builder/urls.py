from django.conf.urls import url
from persona_builder import views

__author__ = 'dipap'


urlpatterns = [
    # persona
    url(r'^personas/create/$', views.create_persona),
    url(r'^personas/(?P<pk>[\w-]+)/edit-properties/$', views.edit_persona_properties),
    url(r'^personas/(?P<pk>[\w-]+)/$', views.view_persona),
    url(r'^personas/(?P<pk>[\w-]+)/delete/$$', views.delete_persona),
    url(r'^personas/(?P<pk>[\w-]+)/update-users/$', views.update_users),

    # list all personas
    url(r'^personas/$', views.list_personas),
]
