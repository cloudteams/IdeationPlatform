# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('connection_type', models.CharField(max_length=128, choices=[(b'django.db.backends.sqlite3', b'SQLite3 file'), (b'django.db.backends.mysql', b'MySQL')])),
                ('info', models.CharField(max_length=8128)),
            ],
        ),
    ]
