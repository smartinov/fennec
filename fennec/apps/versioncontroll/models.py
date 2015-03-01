from django.db import models
from django.conf import settings

CHANGE_TYPE = (
    (0, "ADD"),
    (1, "MODIFY"),
    (2, "REMOVE")
)
SANDBOX_STATUS = (
    (0, "OPEN"),
    (1, "CLOSED")
)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the project")
    description = models.CharField(max_length=512, null=True, help_text="description of the project")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="project author")
    is_deleted = models.BooleanField(default=False)
    percentage_complete = models.CharField(max_length=3, help_text="project complete percentage")
    image_url = models.CharField(max_length=64, help_text="project logo url")
    modification_timestamp = models.DateTimeField(auto_now=True)


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the branch")
    type = models.CharField(max_length=25, help_text="type of branch: feature/hotfix/etc")
    description = models.CharField(max_length=512, help_text="description of the branch")
    current_version = models.IntegerField(default=0)
    project_ref = models.ForeignKey('Project', help_text="project reference")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="branch author")
    parent_branch_revision = models.ForeignKey('BranchRevision', null=True,
                                               help_text="represents a branch revision that is "
                                                         "a starting point of this branch.")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class BranchRevision(models.Model):
    id = models.AutoField(primary_key=True)
    revision_number = models.IntegerField(default=0, help_text="ordinal number of revision")
    previous_revision_ref = models.ForeignKey("BranchRevision", null=True,
                                              help_text="references previous revision of the same branch")
    branch_ref = models.ForeignKey(Branch, null=True, help_text="references owning branch")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")

    @classmethod
    def create(cls, branch_ref):
        branch_revision = BranchRevision(revision_number=0, branch_ref=branch_ref)
        return branch_revision


class Change(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, help_text="change content containing the object of the change")
    object_type = models.CharField(max_length=25, help_text="type of object being changed")
    object_code = models.CharField(max_length=36, help_text="guid, references a concret object being changed")
    change_type = models.IntegerField(choices=CHANGE_TYPE, help_text="defines type of a change")
    is_ui_change = models.BooleanField(default=False, help_text="specifies if change is UI change of db model change")
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="change author")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")

    def get_for_branch_revision(self, branch_rev_id):
        branch_ref = BranchRevision.objects.get(branch_rev_id)
        changes = self.objects.filter(branch_ref)


class SandboxChange(models.Model):
    id = models.AutoField(primary_key=True)
    sandbox_ref = models.ForeignKey('Sandbox', help_text="sandbox reference")
    change_ref = models.ForeignKey('Change', help_text="change reference")
    ordinal = models.IntegerField(default=0, help_text="ordinal number of change in change set")


class BranchRevisionChange(models.Model):
    id = models.AutoField(primary_key=True)
    branch_revision_ref = models.ForeignKey('BranchRevision', help_text="sandbox reference")
    change_ref = models.ForeignKey('Change', help_text="change reference")
    ordinal = models.IntegerField(default=0, help_text="ordinal number of change in change set")


class Sandbox(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   help_text="account who made the sandbox and is its owner of ")
    bound_to_branch_ref = models.ForeignKey('Branch', help_text="references a branch for which the sandbox is used for")
    created_from_branch_revision_ref = models.ForeignKey('BranchRevision', help_text="references branch revision that "
                                                                                     "is 'parent' to the sandbox")
    status = models.SmallIntegerField(choices=SANDBOX_STATUS, default=0,
                                      help_text="state of sandbox, opened or closed")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")
