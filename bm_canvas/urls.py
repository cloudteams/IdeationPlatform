from django.conf.urls import url
from bm_canvas import views

__author__ = 'dipap'


urlpatterns = [
    # project business model canvas
    url(r'^projects/(?P<pk>[\w-]+)/$', views.project_view, name='project-bmc'),
    url(r'^projects/(?P<pk>[\w-]+)/add-entry/$', views.add_entry, name='project-bmc'),
]
