from django.conf.urls import url
from pb_oauth import views

__author__ = 'dipap'


urlpatterns = [
    url(r'^authorize/$', views.authorize),
]
