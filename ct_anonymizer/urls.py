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
    url(r'^admin/', include(admin.site.urls)),

    # anonymizer
    url(r'^anonymizer/', include('anonymizer.urls')),

    # persona builder & authentication
    url(r'^persona-builder/', include('persona_builder.urls')),
    url(r'^persona-builder/', include('pb_oauth.urls')),

    # business model canvas
    url(r'^business-model/', include('bm_canvas.urls')),

    # home page
    url(r'^$', views.index),
]

if settings.DEBUG:
    # media files should only be served from the django server in DEBUG mode
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))
