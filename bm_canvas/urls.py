from django.conf.urls import url
from bm_canvas import views

__author__ = 'dipap'


urlpatterns = [
    # project business model canvas
    url(r'^projects/(?P<pk>[\w-]+)/$', views.project_view, name='project-bmc'),
    url(r'^projects/(?P<pk>[\w-]+)/add-entry/$', views.add_entry, name='add-entry'),

    # entries
    url(r'^entries/update-orders/$', views.update_entry_orders, name='view-entry'),
    url(r'^entries/(?P<pk>[\w-]+)/$', views.view_entry, name='view-entry'),
    url(r'^entries/(?P<pk>[\w-]+)/update/$', views.update_entry, name='update-entry'),
    url(r'^entries/(?P<pk>[\w-]+)/remove/$', views.remove_entry, name='remove-entry'),
]
