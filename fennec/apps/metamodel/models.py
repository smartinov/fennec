__author__ = 'smartinov'
from django.db import models
from django.conf import settings

from fennec.apps.repository.models import BranchRevision

CHANGE_TYPE = (
    (0, "ADD"),
    (1, "MODIFY"),
    (2, "REMOVE")
)

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