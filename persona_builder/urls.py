from django.conf.urls import url
from persona_builder import views, api

__author__ = 'dipap'


urlpatterns = [
    # persona
    url(r'^personas/create/$', views.create_persona),
    url(r'^personas/(?P<pk>[\w-]+)/edit-properties/$', views.edit_persona_properties),
    url(r'^personas/(?P<pk>[\w-]+)/edit-info/$', views.edit_persona_info),
    url(r'^personas/(?P<pk>[\w-]+)/$', views.view_persona),
    url(r'^personas/(?P<pk>[\w-]+)/delete/$$', views.delete_persona),
    url(r'^personas/(?P<pk>[\w-]+)/update-users/$', views.update_users),
    url(r'^propagate/$', views.propagate_persona_placeholder),
    url(r'^perform-pending-action/$', views.perform_pending_action),

    # list all personas
    url(r'^personas/$', views.list_personas),

    # api
    url(r'^api/info/$', api.info),
    url(r'^api/personas/$', api.personas),
    url(r'^api/persona/(?P<pk>[\w-]+)/$', api.persona),
    url(r'^api/init-project/$', api.create_default_persona),
    url(r'^api/campaign-users/$', api.campaign_users),
    url(r'^api/find-user/$', api.find_user),
]
