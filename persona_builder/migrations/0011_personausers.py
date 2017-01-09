# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona_builder', '0010_auto_20151029_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonaUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.TextField()),
                ('persona', models.ForeignKey(to='persona_builder.Persona')),
            ],
        ),
    ]
