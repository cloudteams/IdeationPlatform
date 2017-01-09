# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymizer', '0005_auto_20150916_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionconfiguration',
            name='foreign_keys',
            field=models.TextField(default=b'', editable=False),
        ),
    ]
