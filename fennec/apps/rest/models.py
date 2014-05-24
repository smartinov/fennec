from django.db import models

# Create your models here.

from django.db import models

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,help_text="name of the project")
    description = models.CharField(max_length=512,help_text="description of the project")

    @classmethod
    def create(name, description):
        project = Project(name=name,description=description)
        # do something with the book
        return project
