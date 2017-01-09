# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_canvas', '0007_remove_businessmodelentry_business_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessmodelentry',
            name='fake_fk',
            field=models.ForeignKey(related_name='entries', default=1, to='bm_canvas.BusinessModel'),
            preserve_default=False,
        ),
    ]
