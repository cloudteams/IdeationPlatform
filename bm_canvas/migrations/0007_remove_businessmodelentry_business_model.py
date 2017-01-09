# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_canvas', '0006_auto_20170109_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessmodelentry',
            name='business_model',
        ),
    ]
