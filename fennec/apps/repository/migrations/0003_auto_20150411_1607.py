# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0002_auto_20150308_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMembers',
            fields=[
                ('assignment_id', models.AutoField(serialize=False, primary_key=True)),
                ('member_ref', models.ForeignKey(help_text=b'account reference', to=settings.AUTH_USER_MODEL)),
                ('project_ref', models.ForeignKey(help_text=b'project reference', to='repository.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='change',
            name='made_by',
        ),
        migrations.RemoveField(
            model_name='project',
            name='is_deleted',
        ),
        migrations.AlterField(
            model_name='branchrevisionchange',
            name='change_ref',
            field=models.ForeignKey(help_text=b'change reference', to='metamodel.Change'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='modification_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sandboxchange',
            name='change_ref',
            field=models.ForeignKey(help_text=b'change reference', to='metamodel.Change'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Change',
        ),
    ]
