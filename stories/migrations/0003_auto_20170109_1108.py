# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_auto_20160919_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='persona',
            field=models.ForeignKey(related_name='stories', to='persona_builder.Persona'),
        ),
        migrations.AlterField(
            model_name='story',
            name='state',
            field=models.CharField(max_length=16, choices=[(b'UNSTARTED', b'Unstarted'), (b'STARTED', b'Started'), (b'FINISHED', b'Finished'), (b'DELIVERED', b'Delivered'), (b'ACCEPTED', b'Accepted'), (b'REJECTED', b'Rejected'), (b'RELEASED', b'Released')]),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_type',
            field=models.CharField(default=b'USER_STORY', max_length=16, choices=[(b'USER_STORY', b'User story'), (b'IDEA', b'Idea/Prototype'), (b'EPIC', b'Epic')]),
        ),
    ]
