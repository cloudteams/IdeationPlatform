# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0015_auto_20160226_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='description',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
    ]
