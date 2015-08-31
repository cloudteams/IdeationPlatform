from django.conf.urls import url
from anonymizer import views

__author__ = 'dipap'


urlpatterns = [
    url(r'^test/$', views.test),
]