from uuid import uuid4

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase

from fennec.apps import constants
from fennec.apps.diagram.utils import Table, Schema, Column, Diagram, Layer
from fennec.apps.diagram.serializers import SchemaSerializer, TableSerializer, ColumnSerializer, \
    DiagramSerializer, LayerSerializer
from fennec.apps.versioncontroll.models import Project, Branch, BranchRevision, Sandbox, Change, SandboxChange, \
    BranchRevisionChange
from fennec.apps.versioncontroll import utils
from fennec.apps.versioncontroll.utils import BranchRevisionState, SandboxState


class DefaultAPITest(APITestCase):
    user = None

    def setUp(self):
        user = User.objects.create_superuser(email="test@test.com", username='test', password='test')
        self.client.force_authenticate(user=user)
        all_accounts = self.client.get("/api/users/")
        self.user_url = all_accounts.data[0]['url']
        self.user = user


class UtilsTest(DefaultAPITest):
    def test_retrieval_of_branch_revision_state(self):
        user = User.objects.get(email="test@test.com")
        project = Project(id=1, created_by=self.user)
        project.save()
        branch = Branch(id=1, project_ref=project, created_by=user)
        branch.save()
        branch_revision_1 = BranchRevision(id=1, branch_ref=branch, previous_revision_ref=None, revision_number=0)
        branch_revision_1.save()
        branch_revision_2 = BranchRevision(id=2, branch_ref=branch, previous_revision_ref=branch_revision_1,
                                           revision_number=1)
        branch_revision_2.save()
        branch_revision_3 = BranchRevision(id=3, branch_ref=branch, previous_revision_ref=branch_revision_2,
                                           revision_number=2)
        branch_revision_3.save()

        schema = Schema()
        schema.id = str(uuid4())
        schema.comment = "test"
        schema.database_name = "test db"
        schema.collation = "utf-8"
        serializer = SchemaSerializer(schema)
        json = JSONRenderer().render(serializer.data)
        c = Change()
        c.object_type = 'Schema'
        c.content = json
        c.change_type = 0
        c.object_code = schema.id
        c.is_ui_change = False
        c.made_by = user
        c.save()

        branch_rev_change = BranchRevisionChange()
        branch_rev_change.branch_revision_ref = branch_revision_1
        branch_rev_change.change_ref = c
        branch_rev_change.ordinal = 1
        branch_rev_change.save()

        table = Table(id=str(uuid4()), name="TestTable", collation="utf-8", schema_ref=schema.id)
        table_serializer = TableSerializer(table)
        table_json = JSONRenderer().render(table_serializer.data)

        table_c = Change()
        table_c.object_type = 'Table'
        table_c.content = table_json
        table_c.change_type = 0
        table_c.object_code = table.id
        table_c.is_ui_change = False
        table_c.made_by = user
        table_c.save()

        table_branch_rev_change = BranchRevisionChange()
        table_branch_rev_change.branch_revision_ref = branch_revision_2
        table_branch_rev_change.change_ref = table_c
        table_branch_rev_change.ordinal = 1
        table_branch_rev_change.save()

        column = Column(id=str(uuid4()), name="PK", column_type_ref="123", length=5, ordinal=1, is_primary_key=True,
                        table_ref=table.id)
        column_serializer = ColumnSerializer(column)
        column_json = JSONRenderer().render(column_serializer.data)

        column_c = Change(content=column_json, object_type='Column', change_type=0, object_code=column.id,
                          is_ui_change=False, made_by=user)
        column_c.save()

        column_branch_rev_change = BranchRevisionChange(branch_revision_ref=branch_revision_3, change_ref=column_c,
                                                        ordinal=1)
        column_branch_rev_change.save()

        branch_rev_state = BranchRevisionState(branch_revision_3)

        schemas = branch_rev_state.build_branch_state_metadata()
        self.assertEqual(schemas[0].id, schema.id)
        self.assertEqual(schemas[0].comment, schema.comment)
        self.assertEqual(schemas[0].database_name, schema.database_name)
        self.assertEqual(schemas[0].collation, schema.collation)
        self.assertEqual(schemas[0].tables[0].id, table.id)
        self.assertEqual(schemas[0].tables[0].schema_ref, table.schema_ref)
        self.assertEqual(schemas[0].tables[0].collation, table.collation)
        self.assertEqual(schemas[0].tables[0].name, table.name)
        self.assertEqual(schemas[0].tables[0].columns[0].id, column.id)
        self.assertEqual(schemas[0].tables[0].columns[0].name, column.name)
        self.assertEqual(schemas[0].tables[0].columns[0].column_type_ref, column.column_type_ref)
        self.assertEqual(schemas[0].tables[0].columns[0].length, column.length)
        self.assertEqual(schemas[0].tables[0].columns[0].ordinal, column.ordinal)
        self.assertEqual(schemas[0].tables[0].columns[0].table_ref, column.table_ref)

        table_remove_c = Change(content=table_json, object_type='Table', change_type=2, object_code=table.id,
                                made_by=user, is_ui_change=False)
        table_remove_c.save()

        table_remove_branch_rev_change = BranchRevisionChange()
        table_remove_branch_rev_change.branch_revision_ref = branch_revision_3
        table_remove_branch_rev_change.change_ref = table_remove_c
        table_remove_branch_rev_change.ordinal = 1
        table_remove_branch_rev_change.save()
        schemas = branch_rev_state.build_branch_state_metadata()

        self.assertEqual(schemas[0].id, schema.id)
        self.assertEqual(schemas[0].comment, schema.comment)
        self.assertEqual(schemas[0].database_name, schema.database_name)
        self.assertEqual(schemas[0].collation, schema.collation)
        self.assertEqual(schemas[0].tables, [])

        diagram = Diagram(id=str(uuid4()), name="MainDiagram", description="test diagram")
        diagram_serializer = DiagramSerializer(diagram)
        diagram_json = JSONRenderer().render(diagram_serializer.data)
        diagram_c = Change(content=diagram_json, object_type='Diagram', change_type=0, object_code=table.id,
                           is_ui_change=True, made_by=user)
        diagram_c.save()
        diagram_branch_rev_change = BranchRevisionChange(branch_revision_ref=branch_revision_3, change_ref=diagram_c,
                                                         ordinal=1)
        diagram_branch_rev_change.save()

        diagrams = branch_rev_state.build_branch_state_symbols()
        self.assertEqual(diagrams[0].id, diagram.id)
        self.assertEqual(diagrams[0].name, diagram.name)
        self.assertEqual(diagrams[0].description, diagram.description)


    def test_retrival_of_sandbox_state(self):
        project = Project(id=1, created_by=self.user)
        project.save()
        branch = Branch(id=1, project_ref=project, created_by=self.user)
        branch.save()
        branch_revision_1 = BranchRevision(id=1, branch_ref=branch, previous_revision_ref=None, revision_number=1)
        branch_revision_1.save()
        branch_revision_2 = BranchRevision(id=2, branch_ref=branch, previous_revision_ref=branch_revision_1,
                                           revision_number=2)
        branch_revision_2.save()

        sandbox = Sandbox(created_by=self.user, bound_to_branch_ref=branch,
                          created_from_branch_revision_ref=branch_revision_2)
        sandbox.save()

        schema = Schema(id=str(uuid4()), comment="test", database_name="test_db", collation="utf-8")
        serializer = SchemaSerializer(schema)
        json = JSONRenderer().render(serializer.data)
        change = Change(object_type='Schema', content=json, change_type=0, object_code=schema.id, is_ui_change=False,
                        made_by=self.user)
        change.save()
        branch_rev_change = BranchRevisionChange(branch_revision_ref=branch_revision_1, change_ref=change, ordinal=0)
        branch_rev_change.save()

        table = Table(id=str(uuid4()), name="TestTable", collation="utf-8", schema_ref=schema.id)
        table_serializer = TableSerializer(table)
        table_json = JSONRenderer().render(table_serializer.data)
        table_c = Change(object_type='Table', content=table_json, change_type=0, object_code=table.id,
                         is_ui_change=False, made_by=self.user)
        table_c.save()

        table_sandbox_change = SandboxChange(sandbox_ref=sandbox, change_ref=table_c)
        table_sandbox_change.save()

        util = SandboxState(self.user, sandbox)
        schemas = util.build_sandbox_state_metadata()

        diagram = Diagram(id=str(uuid4()), name="MainDiagram", description="test diagram")
        diagram_serializer = DiagramSerializer(diagram)
        diagram_json = JSONRenderer().render(diagram_serializer.data)
        diagram_c = Change(content=diagram_json, object_type='Diagram', change_type=0, object_code=table.id,
                           is_ui_change=True, made_by=self.user)
        diagram_c.save()
        diagram_branch_rev_change = BranchRevisionChange(branch_revision_ref=branch_revision_2, change_ref=diagram_c,
                                                         ordinal=1)
        diagram_branch_rev_change.save()

        self.assertEqual(schemas[0].id, schema.id)
        self.assertEqual(schemas[0].comment, schema.comment)
        self.assertEqual(schemas[0].database_name, schema.database_name)
        self.assertEqual(schemas[0].collation, schema.collation)
        self.assertEqual(schemas[0].tables[0].id, table.id)
        self.assertEqual(schemas[0].tables[0].schema_ref, table.schema_ref)
        self.assertEqual(schemas[0].tables[0].collation, table.collation)
        self.assertEqual(schemas[0].tables[0].name, table.name)

        layer = Layer(id=str(uuid4()), name="coolstuff", position_x=10, position_y=10, width=10, height=10,
                      diagram_ref=diagram.id, background_color='111333')
        serializer = LayerSerializer(layer)
        layer_json = JSONRenderer().render(serializer.data)
        layer_c = Change(object_type='Layer', content=layer_json, change_type=0, object_code=layer.id,
                         is_ui_change=True,
                         made_by=self.user)
        layer_c.save()
        layer_sandbox_change = SandboxChange(sandbox_ref=sandbox, change_ref=layer_c)
        layer_sandbox_change.save()

        diagrams = util.build_sandbox_state_symbols()

        self.assertEqual(diagrams[0].id, diagram.id)
        self.assertEqual(diagrams[0].name, diagram.name)
        self.assertEqual(diagrams[0].description, diagram.description)

    def test_branch_from_branch_revision(self):
        project = Project(created_by=self.user)
        project.save()
        main_branch = Branch(project_ref=project, name="main", type="main", created_by=self.user)
        main_branch.save()

        main_branch_zero_revision = BranchRevision(branch_ref=main_branch)
        main_branch_zero_revision.save()

        new_branch = utils.branch_from_branch_revision(branch_rev=main_branch_zero_revision, account=self.user,
                                                       name='login_page',
                                                       type='feature', description="login page dev branch")
        self.assertEqual(self.user, new_branch.created_by)
        self.assertEqual(0, new_branch.current_version)
        self.assertEqual(main_branch_zero_revision, new_branch.parent_branch_revision)
        self.assertEqual(project, new_branch.project_ref)
        self.assertEqual('login_page', new_branch.name)
        self.assertEqual('feature', new_branch.type)

        zero_revision = BranchRevision.objects.filter(branch_ref=new_branch).first()

        self.assertIsNotNone(zero_revision)
        self.assertEqual(0, zero_revision.revision_number)
        self.assertEqual(new_branch, zero_revision.branch_ref)


class ProjectTests(APITestCase):
    user_url = ""

    def setUp(self):
        user = User.objects.create_superuser(email="test@test.com", username='test', password='test')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        all_accounts = self.client.get("/api/users/")
        self.user_url = all_accounts.data[0]['url']

    def test_create_project(self):
        """
        Ensure we can create a new project and verify that a 'main' branch was created for it.
        """
        url = "/api/projects/"
        # TODO When url's are fixed, 'created_by' should have a value of 'self.user_url' here...
        data = {'id': 1, 'name': 'TestProject', 'description': 'This is a test', 'created_by': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], data['id'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['created_by'], data['created_by'])

        branches_url = "/api/branches/"
        branch_response = self.client.get(branches_url)
        self.assertEqual(branch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(branch_response.data[0]['id'], 1)
        self.assertEqual(branch_response.data[0]['name'], constants.MASTER_BRANCH_NAME)

    def test_create_branch(self):
        # prepare data
        user = User(id=1)
        user.save()
        project = Project(id=1, created_by=user)
        project.save()

        url = "/api/branches/"
        data = {'id': 1, 'name': 'test_branch', 'type': 'feature', 'description': 'a simple feature branch',
                'current_version': 0, 'project_ref': 1, 'created_by': 1}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], data['id'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['type'], data['type'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['current_version'], data['current_version'])
        self.assertEqual(response.data['project_ref'], data['project_ref'])
        self.assertEqual(response.data['created_by'], data['created_by'])


class UtilsTests(TestCase):
    def test_obtain_sandbox_create_new(self):
        user = User(id=1)
        user.save()
        project = Project(id=1, created_by=user)
        project.save()
        branch = Branch(id=1, project_ref=project, created_by=user)
        branch.save()
        branch_revision_1 = BranchRevision(id=1, branch_ref=branch, revision_number=0)
        branch_revision_1.save()
        branch_revision_2 = BranchRevision(id=1, branch_ref=branch, revision_number=1)
        branch_revision_2.save()
        branch_revision_3 = BranchRevision(id=1, branch_ref=branch, revision_number=2)
        branch_revision_3.save()

        sandbox = utils.obtain_sandbox(user, branch.id)
        self.assertEqual(sandbox.created_by, user)
        self.assertEqual(sandbox.bound_to_branch_ref, branch)
        self.assertEqual(sandbox.created_from_branch_revision_ref, branch_revision_3)
        self.assertEqual(sandbox.status, 0)

    def test_obtain_sandbox_create_new(self):
        user = User(id=1)
        user.save()
        project = Project(id=1, created_by=user)
        project.save()
        branch = Branch(id=1, project_ref=project, created_by=user)
        branch.save()
        branch_revision_1 = BranchRevision(id=1, branch_ref=branch, revision_number=0)
        branch_revision_1.save()
        branch_revision_2 = BranchRevision(id=1, branch_ref=branch, revision_number=1)
        branch_revision_2.save()
        branch_revision_3 = BranchRevision(id=1, branch_ref=branch, revision_number=2)
        branch_revision_3.save()

        sandbox = utils.obtain_sandbox(user, branch.id)
        self.assertEqual(sandbox.created_by, user)
        self.assertEqual(sandbox.bound_to_branch_ref, branch)
        self.assertEqual(sandbox.created_from_branch_revision_ref, branch_revision_3)
        self.assertEqual(sandbox.status, 0)


class SandboxAPITests(APITestCase):
    user_url = ""

    def setUp(self):
        user = User.objects.create_superuser(email="test@test.com", username='test', password='test')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        all_accounts = self.client.get("/api/users/")
        self.user_url = all_accounts.data[0]['url']


    def test_build_sandbox_state(self):
        pass



