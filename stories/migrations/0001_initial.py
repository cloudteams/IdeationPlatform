# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0021_persona_is_processing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('project_id', models.IntegerField()),
                ('project_name', models.CharField(max_length=1023)),
                ('owner', models.TextField()),
                ('project_scenario_id', models.SmallIntegerField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('tags', models.TextField(blank=True)),
                ('comments', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('project_id', models.IntegerField()),
                ('project_name', models.CharField(max_length=1023)),
                ('owner', models.TextField()),
                ('project_story_id', models.SmallIntegerField()),
                ('title', models.TextField()),
                ('story_type', models.CharField(max_length=16, choices=[(b'USER_STORY', b'User story'), (b'IDEA', b'Idea/Prototype'), (b'EPIC', b'Epic')])),
                ('role', models.TextField()),
                ('purpose', models.TextField()),
                ('target', models.TextField()),
                ('acceptance_criteria', models.TextField(blank=True)),
                ('comments', models.TextField(blank=True)),
                ('priority', models.SmallIntegerField()),
                ('estimate', models.SmallIntegerField()),
                ('state', models.CharField(max_length=16, choices=[(b'STARTED', b'Started'), (b'FINISHED', b'Finished'), (b'DELIVERED', b'Delivered'), (b'ACCEPTED', b'Accepted'), (b'REJECTED', b'Rejected'), (b'RELEASED', b'Released')])),
                ('persona', models.ForeignKey(to='persona_builder.Persona')),
                ('scenarios', models.ManyToManyField(to='stories.Scenario')),
            ],
        ),
    ]
