# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0021_persona_is_processing'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 27, 9, 38, 26, 788000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 27, 9, 38, 32, 591000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
