# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0018_persona_based_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='personausers',
            name='info',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
