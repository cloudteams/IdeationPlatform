# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0006_auto_20150916_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=None, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='persona',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=False),
        ),
    ]
