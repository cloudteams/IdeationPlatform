# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymizer', '0002_connectionconfiguration_users_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionconfiguration',
            name='total',
            field=models.CharField(default=b'', max_length=16384),
        ),
    ]
