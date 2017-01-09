# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0013_persona_campaign_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
