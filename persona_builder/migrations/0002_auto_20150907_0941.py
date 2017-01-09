# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='is_ready',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='persona',
            name='avatar',
            field=models.ImageField(upload_to=b'persona-avatars'),
        ),
    ]
