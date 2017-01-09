# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0020_remove_persona_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='is_processing',
            field=models.BooleanField(default=False),
        ),
    ]
