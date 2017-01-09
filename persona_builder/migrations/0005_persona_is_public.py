# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0004_auto_20150907_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
