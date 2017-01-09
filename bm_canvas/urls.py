from django.conf.urls import url
from bm_canvas import views

__author__ = 'dipap'


urlpatterns = [
    # all canvases list
    url(r'^projects/(?P<pk>[\w-]+)/$', views.project_view, name='project-bmc'),
    url(r'^projects/(?P<pk>[\w-]+)/create/$', views.create_canvas, name='project-bmc-create'),

    # project business model canvas
    url(r'^projects/(?P<pk>[\w-]+)/(?P<bm>[\w-]+)/$', views.canvas_view, name='canvas-bmc'),
    url(r'^projects/(?P<pk>[\w-]+)/(?P<bm>[\w-]+)/add-entry/$', views.add_entry, name='add-entry'),

    # autocomplete
    url(r'^projects/(?P<pk>[\w-]+)/(?P<bm>[\w-]+)/suggest-term/$', views.suggest_term, name='suggest-term'),

    # entries
    url(r'^entries/update-orders/$', views.update_entry_orders, name='view-entry'),
    url(r'^entries/(?P<pk>[\w-]+)/$', views.view_entry, name='view-entry'),
    url(r'^entries/(?P<pk>[\w-]+)/update/$', views.update_entry, name='update-entry'),
    url(r'^entries/(?P<pk>[\w-]+)/remove/$', views.remove_entry, name='remove-entry'),
]
