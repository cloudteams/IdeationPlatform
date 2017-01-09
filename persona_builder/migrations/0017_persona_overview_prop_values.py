# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0016_auto_20160330_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='overview_prop_values',
            field=models.TextField(default=b'[]', editable=False),
        ),
    ]
