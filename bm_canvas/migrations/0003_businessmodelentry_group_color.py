# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_canvas', '0002_businessmodelentry_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessmodelentry',
            name='group_color',
            field=models.CharField(default=b'#FFFFFF', max_length=7),
        ),
    ]
