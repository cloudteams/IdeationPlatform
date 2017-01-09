# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymizer', '0004_auto_20150904_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionconfiguration',
            name='properties',
            field=models.TextField(default=b''),
        ),
    ]
