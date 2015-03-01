import os
from unittest.case import TestCase
from django.contrib.auth.models import User
from fennec.apps.integration.parsers.mysql.workbench.parser import WorkbenchParser
from fennec.apps.integration.importer.importer import FennecImporter
from fennec.apps.versioncontroll.models import Change, Project, Branch, BranchRevisionChange, BranchRevision
from fennec.apps.versioncontroll.utils import BranchRevisionState

__author__ = 'Darko'


class FennecImporterTest(TestCase):

    def test_import_from_file(self):
        user = User()
        user.username = 'test'
        user.save()

        project = Project()
        project.created_by = user
        project.name = "test"
        project.save()

        branch = Branch()
        branch.name = "main"
        branch.project_ref = project
        branch.created_by = user
        branch.save()

        zero_rev = BranchRevision()
        zero_rev.revision_number = 0
        zero_rev.branch_ref = branch
        zero_rev.save()



        path = self.get_path('samplemodel.mwb')
        parser = WorkbenchParser()
        model = parser.parse_file(path)
        importer = FennecImporter(model=model, user=user, branch_rev=zero_rev)
        importer.import_model()

        # changes = Change.objects.all()
        # for c in changes:
        #     print str(c.content)
        state_builder = BranchRevisionState(branch_rev=zero_rev)
        metadata = state_builder.build_branch_state_metadata()

    @staticmethod
    def get_path(path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', path.lstrip('/'))