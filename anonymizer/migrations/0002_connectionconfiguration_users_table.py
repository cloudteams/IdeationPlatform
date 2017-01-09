# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionconfiguration',
            name='users_table',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
