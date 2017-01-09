# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_canvas', '0005_auto_20170109_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessmodel',
            name='id',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='businessmodel',
            name='project_id',
            field=models.IntegerField(),
        ),
    ]
