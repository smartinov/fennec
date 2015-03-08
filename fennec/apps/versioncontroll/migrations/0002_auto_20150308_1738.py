# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('versioncontroll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image_url',
            field=models.CharField(help_text=b'project logo url', max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='modification_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 8, 17, 38, 34, 729000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='percentage_complete',
            field=models.FloatField(default=0, help_text=b'project complete percentage'),
            preserve_default=True,
        ),
    ]
