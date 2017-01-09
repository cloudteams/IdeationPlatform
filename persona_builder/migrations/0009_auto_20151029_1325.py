# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0008_auto_20150916_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='owner',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
