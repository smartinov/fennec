# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'name of the branch', max_length=64)),
                ('type', models.CharField(help_text=b'type of branch: feature/hotfix/etc', max_length=25)),
                ('description', models.CharField(help_text=b'description of the branch', max_length=512)),
                ('current_version', models.IntegerField(default=0)),
                ('is_deleted', models.SmallIntegerField(default=0, help_text=b'logical deletion')),
                ('created_by', models.ForeignKey(help_text=b'branch author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BranchRevision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('revision_number', models.IntegerField(default=0, help_text=b'ordinal number of revision')),
                ('is_deleted', models.SmallIntegerField(default=0, help_text=b'logical deletion')),
                ('branch_ref', models.ForeignKey(to='versioncontroll.Branch', help_text=b'references owning branch', null=True)),
                ('previous_revision_ref', models.ForeignKey(to='versioncontroll.BranchRevision', help_text=b'references previous revision of the same branch', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BranchRevisionChange',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('ordinal', models.IntegerField(default=0, help_text=b'ordinal number of change in change set')),
                ('branch_revision_ref', models.ForeignKey(help_text=b'sandbox reference', to='versioncontroll.BranchRevision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.CharField(help_text=b'change content containing the object of the change', max_length=255)),
                ('object_type', models.CharField(help_text=b'type of object being changed', max_length=25)),
                ('object_code', models.CharField(help_text=b'guid, references a concret object being changed', max_length=36)),
                ('change_type', models.IntegerField(help_text=b'defines type of a change', choices=[(0, b'ADD'), (1, b'MODIFY'), (2, b'REMOVE')])),
                ('is_ui_change', models.BooleanField(default=False, help_text=b'specifies if change is UI change of db model change')),
                ('is_deleted', models.SmallIntegerField(default=0, help_text=b'logical deletion')),
                ('made_by', models.ForeignKey(help_text=b'change author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'name of the project', max_length=64)),
                ('description', models.CharField(help_text=b'description of the project', max_length=512, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(help_text=b'project author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sandbox',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.SmallIntegerField(default=0, help_text=b'state of sandbox, opened or closed', choices=[(0, b'OPEN'), (1, b'CLOSED')])),
                ('is_deleted', models.SmallIntegerField(default=0, help_text=b'logical deletion')),
                ('bound_to_branch_ref', models.ForeignKey(help_text=b'references a branch for which the sandbox is used for', to='versioncontroll.Branch')),
                ('created_by', models.ForeignKey(help_text=b'account who made the sandbox and is its owner of ', to=settings.AUTH_USER_MODEL)),
                ('created_from_branch_revision_ref', models.ForeignKey(help_text=b"references branch revision that is 'parent' to the sandbox", to='versioncontroll.BranchRevision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SandboxChange',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('ordinal', models.IntegerField(default=0, help_text=b'ordinal number of change in change set')),
                ('change_ref', models.ForeignKey(help_text=b'change reference', to='versioncontroll.Change')),
                ('sandbox_ref', models.ForeignKey(help_text=b'sandbox reference', to='versioncontroll.Sandbox')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='branchrevisionchange',
            name='change_ref',
            field=models.ForeignKey(help_text=b'change reference', to='versioncontroll.Change'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='parent_branch_revision',
            field=models.ForeignKey(to='versioncontroll.BranchRevision', help_text=b'represents a branch revision that is a starting point of this branch.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='project_ref',
            field=models.ForeignKey(help_text=b'project reference', to='versioncontroll.Project'),
            preserve_default=True,
        ),
    ]
