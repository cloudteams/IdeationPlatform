# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('project_name', models.CharField(max_length=1023)),
            ],
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='story',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='story',
            name='project_name',
        ),
        migrations.AlterField(
            model_name='story',
            name='scenarios',
            field=models.ManyToManyField(related_name='stories', to='stories.Scenario'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='project',
            field=models.ForeignKey(related_name='project_scenarios', default=None, to='stories.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='story',
            name='project',
            field=models.ForeignKey(related_name='project_stories', default=None, to='stories.Project'),
            preserve_default=False,
        ),
    ]
