# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from bm_canvas.models import BusinessModel, BusinessModelEntry


def new_pks(apps, schema_editor):
    for idx, bm in enumerate(BusinessModel.objects.all()):
        bm.id = idx + 1
        bm.save()
        bm.entries.update(fake_fk=bm.id)


class Migration(migrations.Migration):

    dependencies = [
        ('bm_canvas', '0004_auto_20170109_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessmodel',
            name='id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='businessmodelentry',
            name='fake_fk',
            field=models.IntegerField(null=True),
        ),
        migrations.RunPython(new_pks),
    ]
