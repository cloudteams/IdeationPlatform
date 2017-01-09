# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_canvas', '0008_auto_20170109_1152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businessmodelentry',
            old_name='fake_fk',
            new_name='business_model',
        ),
    ]
