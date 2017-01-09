# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0005_persona_is_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='id',
        ),
        migrations.AddField(
            model_name='persona',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
    ]
