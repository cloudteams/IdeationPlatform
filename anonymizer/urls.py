from django.conf.urls import url
import views

__author__ = 'dipap'


urlpatterns = [
    # connection urls
    url(r'^connection/create/$', views.create_configuration),
    url(r'^connection/update-info/(?P<pk>\d+)/sqlite3/$', views.sqlite3_info),
]
