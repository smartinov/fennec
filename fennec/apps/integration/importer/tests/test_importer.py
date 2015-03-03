import os
from unittest.case import TestCase
from django.contrib.auth.models import User
from fennec.apps.integration.parsers.mysql.workbench.parser import WorkbenchParser
from fennec.apps.integration.importer.importer import FennecImporter
from fennec.apps.versioncontroll.models import Change, Project, Branch, BranchRevisionChange, BranchRevision
from fennec.apps.versioncontroll.utils import BranchRevisionState
import time
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

        start_of_parsing = int(round(time.time() * 1000))


        path = self.get_path('samplemodel.mwb')
        parser = WorkbenchParser()
        model = parser.parse_file(path)

        end_of_parsing = int(round(time.time() * 1000))

        importer = FennecImporter(model=model, user=user, branch_rev=zero_rev)
        importer.import_model()

        end_of_import = int(round(time.time() * 1000))

        state_builder = BranchRevisionState(branch_rev=zero_rev)
        metadata = state_builder.build_branch_state_metadata()

        end_of_build= int(round(time.time() * 1000))
        print "Schema:" + metadata[0].database_name
        print "number of tables: " + str(len(metadata[0].tables))
        print "Parsing time:" + str(end_of_parsing - start_of_parsing)
        print "Importing time:" + str(end_of_import - end_of_parsing)
        print "State build time:" + str(end_of_build - end_of_import)

    @staticmethod
    def get_path(path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', path.lstrip('/'))