# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0009_auto_20151029_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'persona-avatars', blank=True),
        ),
    ]
