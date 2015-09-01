from django.conf.urls import url
from anonymizer import views
from anonymizer.views import ConnectionConfigurationCreateView

__author__ = 'dipap'


urlpatterns = [
    url(r'^connection/create/$', ConnectionConfigurationCreateView.as_view()),
    url(r'^connection/update-info/(?P<pk>\d+)/'),
]
