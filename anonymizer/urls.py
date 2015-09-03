from django.conf.urls import url
import views

__author__ = 'dipap'


urlpatterns = [
    # home page of the tool
    url(r'^$', views.home),

    # connection urls
    url(r'^connection/create/$', views.create_configuration),

    # different connection types
    url(r'^connection/update-info/(?P<pk>\d+)/sqlite3/$', views.sqlite3_info),
    url(r'^connection/update-info/(?P<pk>\d+)/mysql/$', views.mysql_info),

    # pick user table & columns
    url(r'^connection/(?P<pk>\d+)/suggest-user-table/$', views.suggest_users_table),
    url(r'^connection/(?P<pk>\d+)/select-columns/$', views.select_columns),

    # manual update
    url(r'^connection/(?P<pk>\d+)/edit/$', views.update_configuration),

    # query & console to run them
    url(r'^connection/(?P<pk>\d+)/query/$', views.query_connection),
    url(r'^connection/(?P<pk>\d+)/console/$', views.console),
]
