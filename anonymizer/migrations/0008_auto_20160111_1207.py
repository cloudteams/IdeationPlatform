# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymizer', '0007_connectionconfiguration_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionconfiguration',
            name='connection_type',
            field=models.CharField(max_length=128, choices=[(b'django.db.backends.sqlite3', b'SQLite3 file'), (b'django.db.backends.mysql', b'MySQL'), (b'django.db.backends.psycopg2', b'Postgres')]),
        ),
    ]
