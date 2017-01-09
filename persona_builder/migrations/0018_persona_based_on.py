# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0017_persona_overview_prop_values'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='based_on',
            field=models.ForeignKey(default=None, blank=True, to='persona_builder.Persona', null=True),
        ),
    ]
