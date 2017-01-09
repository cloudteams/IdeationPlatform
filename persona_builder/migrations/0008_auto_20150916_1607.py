# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0007_auto_20150916_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='query',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='persona',
            name='users',
            field=models.TextField(default=b'[]', editable=False),
        ),
    ]
