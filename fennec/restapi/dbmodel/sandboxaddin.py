from fennec.restapi.dbmodel.models import Sandbox

__author__ = 'Darko'


class SandboxAddin():
    def pre_save(self, obj):
        user = self.request.user
        branch_id = self.request.DATA['branch_id']
        obj.sandbox_ref = Sandbox.obtain_sandbox(user, branch_id)
