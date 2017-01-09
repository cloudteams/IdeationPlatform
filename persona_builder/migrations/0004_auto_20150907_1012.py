# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0003_auto_20150907_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='properties',
        ),
        migrations.AddField(
            model_name='persona',
            name='query',
            field=models.CharField(default='', max_length=4096, editable=False),
            preserve_default=False,
        ),
    ]
