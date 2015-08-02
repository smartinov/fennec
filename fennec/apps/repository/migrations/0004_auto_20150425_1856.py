# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20150411_1607'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectMembers',
            new_name='ProjectMember',
        ),
        migrations.RenameField(
            model_name='projectmember',
            old_name='assignment_id',
            new_name='id',
        ),
    ]
