# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0014_auto_20160223_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personausers',
            name='user_id',
            field=models.IntegerField(db_index=True),
        ),
    ]
