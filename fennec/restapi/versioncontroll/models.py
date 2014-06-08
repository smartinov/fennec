from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models.sql.datastructures import DateTime
CHANGE_TYPE = (
    (0, 'ADD'),
    (1, 'REMOVE'),
    (2, 'MODIFY'),
)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the project")
    description = models.CharField(max_length=512, help_text="description of the project")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="project author")
    is_deleted = models.BooleanField(default=False)


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the branch")
    type = models.CharField(max_length=25, help_text="type of branch: feature/hotfix/etc")
    description = models.CharField(max_length=512, help_text="description of the branch")
    current_version = models.IntegerField(default=0)
    project_ref = models.ForeignKey(Project, help_text="project reference")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="branch author")


class BranchRevision(models.Model):
    id = models.AutoField(primary_key=True)
    revision_number = models.IntegerField(default=0, help_text="ordinal number of revision")
    previous_revision_ref = models.ForeignKey("BranchRevision", null=True,
                                              help_text="references previous revision of the same branch")
    branch_ref = models.ForeignKey(Branch, null=True, help_text="references owning branch")


class ChangeSet(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255, help_text="comment eh")
    branch_revision_ref = models.ForeignKey(BranchRevision, help_text="revision reference")
    submitted_on = models.DateTimeField(auto_now_add=True, blank=True, help_text="datetime of submission")
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="change author")


class Change(models.Model):
    id = models.AutoField(primary_key=True)
    ordinal = models.IntegerField(default=0, help_text="ordinal number of change in change set")
    command_text = models.CharField(max_length=255, help_text="command text containing the object of the change")
    object_type = models.CharField(max_length=25, help_text="type of object being changed")
    object_ref = models.IntegerField(default=-1, help_text="references concrete object being changed")
    change_type = models.IntegerField(choices=CHANGE_TYPE, help_text="defines type of a change")
    is_ui_change = models.BooleanField(default=False, help_text="specifies if change is UI change of db model change")
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="change author")
    change_set_ref = models.ForeignKey(ChangeSet, help_text="change set reference")


    #def create_change(self, change):


class Sandbox(models.Model):
    id = models.AutoField(primary_key=True)
    branch_ref = models.ForeignKey(Branch, help_text="references a branch for which the sandbox is used for")
    accounts = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      help_text="references all accounts who have access and who can make changenes in this sandbox")

    @staticmethod
    def obtain_sandbox(user, branch_id):
        branch = Branch.objects.get(pk=int(branch_id))
        sandbox = Sandbox.objects.filter(branch_ref=branch, accounts__id=user.id).first()
        if sandbox is None:
            sandbox = Sandbox()
            sandbox.branch_ref = branch
            sandbox.save()
            sandbox.accounts.add(user)
            sandbox.save()
        return sandbox