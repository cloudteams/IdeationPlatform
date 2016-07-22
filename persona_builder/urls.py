from django.conf.urls import url
from persona_builder import views, api

__author__ = 'dipap'


urlpatterns = [
    # list personas in campaign & all public personas
    url(r'^personas/$', views.list_personas),
    url(r'^personas/pool/$', views.pool),

    # clone persona
    url(r'^personas/add-from-pool/(?P<pk>[\w-]+)/$', views.add_from_pool),

    # persona operations
    url(r'^personas/create/$', views.create_persona),
    url(r'^personas/(?P<pk>[\w-]+)/edit-properties/$', views.edit_persona_properties),
    url(r'^personas/(?P<pk>[\w-]+)/edit-info/$', views.edit_persona_info),
    url(r'^personas/(?P<pk>[\w-]+)/$', views.view_persona),
    url(r'^personas/(?P<pk>[\w-]+)/delete/$$', views.delete_persona),
    url(r'^personas/(?P<pk>[\w-]+)/update-users/$', views.update_users),
    url(r'^personas/(?P<pk>[\w-]+)/load-users/$', views.get_persona_users),
    url(r'^propagate/$', views.propagate_persona_placeholder),
    url(r'^perform-pending-action/$', views.perform_pending_action),

    # api
    url(r'^api/info/$', api.info),
    url(r'^api/personas/$', api.personas),
    url(r'^api/persona/(?P<pk>[\w-]+)/$', api.persona),
    url(r'^api/init-project/$', api.create_default_persona),
    url(r'^api/campaign-users/$', api.campaign_users),
    url(r'^api/find-user/$', api.find_user),
]
