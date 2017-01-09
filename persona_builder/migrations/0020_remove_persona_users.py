# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0019_personausers_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='users',
        ),
    ]
