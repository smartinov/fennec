from django.db import models
from django.conf import settings
# Create your models here.

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the project")
    description = models.CharField(max_length=512, help_text="description of the project")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="project author")

    @classmethod
    def create(name, description):
        project = Project(name=name, description=description)
        # do something with the book
        return project


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the branch")
    type = models.CharField(max_length=25, help_text="type of branch: feature/hotfix/etc")
    description = models.CharField(max_length=512, help_text="description of the branch")
    current_version = models.IntegerField(default=0)
    project_ref = models.ForeignKey('Project', help_text="project reference")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="branch author")