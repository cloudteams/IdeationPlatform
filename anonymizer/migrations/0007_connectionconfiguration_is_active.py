# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymizer', '0006_connectionconfiguration_foreign_keys'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionconfiguration',
            name='is_active',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
