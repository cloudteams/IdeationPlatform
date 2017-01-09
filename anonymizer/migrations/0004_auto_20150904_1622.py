# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymizer', '0003_connectionconfiguration_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connectionconfiguration',
            name='total',
        ),
        migrations.AddField(
            model_name='connectionconfiguration',
            name='properties',
            field=models.CharField(default=b'', max_length=16384),
        ),
        migrations.AddField(
            model_name='connectionconfiguration',
            name='user_pk',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
