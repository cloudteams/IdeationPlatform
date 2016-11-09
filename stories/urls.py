from django.conf.urls import url
from stories import views

__author__ = 'dipap'


urlpatterns = [
    # project
    url(r'^projects/(?P<project_id>[\w-]+)/$', views.project_view, name='project-stories'),

    # scenario
    url(r'^projects/(?P<project_id>[\w-]+)/add-scenario/$', views.add_scenario, name='add-scenario'),
    url(r'^projects/(?P<project_id>[\w-]+)/scenarios/(?P<scenario_id>[\w-]+)/$', views.scenario_details,
        name='scenario-details'),
    url(r'^projects/(?P<project_id>[\w-]+)/scenarios/(?P<scenario_id>[\w-]+)/edit/$', views.edit_scenario,
        name='edit-scenario'),
    url(r'^projects/(?P<project_id>[\w-]+)/scenarios/(?P<scenario_id>[\w-]+)/delete/$', views.delete_scenario,
        name='delete-scenario'),

    # story
    url(r'^projects/(?P<project_id>[\w-]+)/scenarios/(?P<scenario_id>[\w-]+)/add-story/$',
        views.add_story, name='add-story-in-scenario'),
    url(r'^projects/(?P<project_id>[\w-]+)/stories/(?P<story_id>[\w-]+)/$', views.story_details,
        name='story-details'),
    url(r'^projects/(?P<project_id>[\w-]+)/stories/(?P<story_id>[\w-]+)/edit/$', views.edit_story,
        name='edit-story'),
    url(r'^projects/(?P<project_id>[\w-]+)/stories/(?P<story_id>[\w-]+)/delete/$', views.delete_story,
        name='delete-story'),

    # add existing story to scenario
    url(r'^scenarios/(?P<scenario_id>[\w-]+)/stories-to-add/$', views.stories_to_add, name='stories-to-add'),
    url(r'^scenarios/(?P<scenario_id>[\w-]+)/add-story/$', views.add_story_to_scenario, name='add-existing-story'),
]
