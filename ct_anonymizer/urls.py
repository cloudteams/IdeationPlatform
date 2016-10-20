"""ct_anonymizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
import views
from ct_anonymizer import settings

urlpatterns = [
    url(r'^team-ideation-tools/admin/', include(admin.site.urls)),

    # anonymizer
    url(r'^team-ideation-tools/anonymizer/', include('anonymizer.urls')),

    # persona builder & authentication
    url(r'^team-ideation-tools/', include('persona_builder.urls')),
    url(r'^team-ideation-tools/', include('pb_oauth.urls')),

    # business model canvas
    url(r'^team-ideation-tools/business-model/', include('bm_canvas.urls')),

    # stories
    url(r'^team-ideation-tools/requirements-library/', include('stories.urls')),

    # home page
    url(r'^team-ideation-tools/$', views.index),
]

# media files should only be served from the django server in DEBUG mode
# todo fix
urlpatterns += patterns('',
                        (r'^team-ideation-tools/media/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.MEDIA_ROOT}))
