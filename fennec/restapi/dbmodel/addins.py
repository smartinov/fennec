from fennec.restapi.dbmodel.models import Sandbox
from fennec.restapi.dbmodel.models import Change
from serializers import serialize

__author__ = 'Darko'

changes = {}

class SandboxAddin():
    def pre_save(self, obj):
        user = self.request.user
        branch_id = self.request.DATA['branch_id']
        obj.sandbox_ref = Sandbox.obtain_sandbox(user, branch_id)

class ChangeAddin():

    def post_save(self, obj, created=False):
        user = self.request.user
        change = Change()
        change.made_by = user
        change.change_type = 0 if created else 1
        change.command_text = serialize(obj)
        change.is_ui_change = False
        change.object_ref = obj.id
        change.object_type = obj.__class__.__name__
        key = "{0}:{1}".format(change.object_type, change.object_ref)
        changes[key] = change
        change.save()
        print 'total changes {0}'.format(len(changes))

    def post_delete(self, obj):
        user = self.request.user
        change = Change()
        change.made_by = user
        change.change_type = 2
        change.command_text = serialize(obj)
        change.is_ui_change = False
        change.object_type = obj.__class__.__name__
        change.object_ref = obj.id

        key = "{0}:{1}".format(change.object_type, change.object_ref)
        changes[key] = change
        print 'post_delete {0}'.format(len(changes))