# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0011_personausers'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='project_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
