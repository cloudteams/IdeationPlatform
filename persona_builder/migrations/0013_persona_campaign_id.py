# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0012_persona_project_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='campaign_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
