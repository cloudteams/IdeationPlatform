# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessModel',
            fields=[
                ('project_id', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('project_name', models.CharField(max_length=1023)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessModelEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255)),
                ('section', models.CharField(max_length=255, choices=[(b'KP', b'Key Partners'), (b'KA', b'Key Activities'), (b'KR', b'Key Resources'), (b'VP', b'Value Propositions'), (b'CR', b'Customer Relationships'), (b'CH', b'Channels'), (b'CS', b'Customer Segments'), (b'C$', b'Cost Structure'), (b'R$', b'Revenue Streams')])),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('business_model', models.ForeignKey(related_name='entries', to='bm_canvas.BusinessModel')),
            ],
        ),
    ]
