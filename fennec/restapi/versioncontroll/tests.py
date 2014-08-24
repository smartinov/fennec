import StringIO
from uuid import uuid4
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from fennec.restapi.dbmodel.models import Table, Namespace, Schema, Column, Diagram
from fennec.restapi.dbmodel.serializers import NamespaceSerializer, SchemaSerializer, TableSerializer, ColumnSerializer, DiagramSerializer
from fennec.restapi.versioncontroll.models import Project, Branch, BranchRevision, Sandbox, Change, SandboxChange, BranchRevisionChange
from fennec.restapi.versioncontroll import utils
from fennec.restapi.versioncontroll.serializers import ChangeSerializer
from fennec.restapi.versioncontroll.utils import BranchRevisionState


class DefaultAPITests(APITestCase):
    def setUp(self):
        user = User.objects.create_superuser(email="test@test.com", username='test', password='test')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        all_accounts = self.client.get("/api/users/")
        self.user_url = all_accounts.data[0]['url']


class UtilsTest(DefaultAPITests):
    def test_retrieval_of_branch_revision_state(self):
        user = User.objects.get(email="test@test.com")
        project = Project(id=1, created_by=user)
        project.save()
        branch = Branch(id=1, project_ref=project, created_by=user)
        branch.save()
        branch_revision_1 = BranchRevision(id=1, branch_ref=branch, revision_number=0)
        branch_revision_1.save()
        branch_revision_2 = BranchRevision(id=2, branch_ref=branch, revision_number=1)
        branch_revision_2.save()
        branch_revision_3 = BranchRevision(id=3, branch_ref=branch, revision_number=2)
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
                          is_ui_change=False,made_by=user)
        column_c.save()

        column_branch_rev_change = BranchRevisionChange(branch_revision_ref=branch_revision_3, change_ref=column_c, ordinal=1)
        column_branch_rev_change.save()

        branch_rev_state = BranchRevisionState(branch_revision_3)

        schemas = branch_rev_state.build_state_metadata()
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


        table_remove_c = Change(content=table_json, object_type='Table', change_type=2, object_code=table.id, made_by=user, is_ui_change=False)
        table_remove_c.save()

        table_remove_branch_rev_change = BranchRevisionChange()
        table_remove_branch_rev_change.branch_revision_ref = branch_revision_3
        table_remove_branch_rev_change.change_ref = table_remove_c
        table_remove_branch_rev_change.ordinal = 1
        table_remove_branch_rev_change.save()
        schemas = branch_rev_state.build_state_metadata()

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
        diagram_branch_rev_change = BranchRevisionChange(branch_revision_ref=branch_revision_3, change_ref=diagram_c, ordinal=1)
        diagram_branch_rev_change.save()


        diagrams = branch_rev_state.build_state_symbols()
        self.assertEqual(diagrams[0].id, diagram.id)
        self.assertEqual(diagrams[0].name, diagram.name)
        self.assertEqual(diagrams[0].description, diagram.description)
        

        diagrams = branch_rev_state.build_state_metadata()


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
        #TODO When url's are fixed, 'created_by' should have a value of 'self.user_url' here...
        data = {'id': 1, 'name': 'TestProject', 'description': 'This is a test', 'created_by': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], data['id'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['created_by'], data['created_by'])

        branches_url = "/api/projects/1/branches/"
        branch_response = self.client.get(branches_url)
        self.assertEqual(branch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(branch_response.data[0]['id'], 1)
        self.assertEqual(branch_response.data[0]['name'], 'main')

    def test_create_branch(self):
        #prepare data
        user = User(id=1)
        user.save()
        project = Project(id=1, created_by=user)
        project.save()

        url = "/api/projects/1/branches/"
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

    def test_retrieve_project_branches(self):
        '''
        Retrieval of branches via /project/{id}/branches/ should return only branches that belong to that project.
        '''
        user = User(id=1)
        user.save()
        project_one = Project(id=1, created_by=user)
        project_one.save()
        project_two = Project(id=2, created_by=user)
        project_two.save()
        branch_one = Branch(id=1, created_by=user, project_ref=project_one)
        branch_one.save()
        branch_two = Branch(id=2, created_by=user, project_ref=project_two)
        branch_two.save()
        branch_three = Branch(id=3, created_by=user, project_ref=project_two)
        branch_three.save()

        p1_branches_url = "/api/projects/{}/branches/".format(project_one.id)
        p1_branches_response = self.client.get(p1_branches_url)
        self.assertEqual(p1_branches_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(p1_branches_response.data), 1)
        self.assertEqual(p1_branches_response.data[0]['id'], branch_one.id)
        self.assertEqual(p1_branches_response.data[0]['project_ref'], project_one.id)

        p2_branches_url = "/api/projects/{}/branches/".format(project_two.id)
        p2_branches_response = self.client.get(p2_branches_url)
        self.assertEqual(p2_branches_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(p2_branches_response.data), 2)
        self.assertEqual(p2_branches_response.data[0]['id'], branch_two.id)
        self.assertEqual(p2_branches_response.data[0]['project_ref'], project_two.id)
        self.assertEqual(p2_branches_response.data[1]['id'], branch_three.id)
        self.assertEqual(p2_branches_response.data[1]['project_ref'], project_two.id)


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


    def test_post_change(self):
        """
        Test posting of a change on sandbox controller.
        Verify that change and assignment table entry have been created.
        """
        login_res = self.client.login(username="test", password="test")
        self.assertTrue(login_res)

        user = User.objects.filter(username="test").first()

        project = Project(id=1, created_by=user)
        project.save()
        branch_one = Branch(id=1, created_by=user, project_ref=project)
        branch_one.save()
        branch_rev = BranchRevision(id=1, branch_ref=branch_one, revision_number=0)
        branch_rev.save()

        sandbox = Sandbox(id=1)
        sandbox.created_by = user
        sandbox.bound_to_branch_ref = branch_one
        sandbox.created_from_branch_revision_ref = branch_rev
        sandbox.save()

        branches_url = "/api/projects/{}/branches/".format(project.id)
        branches_response = self.client.get(branches_url)
        self.assertEqual(branches_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(branches_response.data), 1)
        self.assertEqual(branches_response.data[0]['id'], branch_one.id)
        self.assertEqual(branches_response.data[0]['project_ref'], project.id)

        change_creating_url = "/api/sandboxes/1/change/"

        object_code = str(uuid4())
        content = {
            "id": 1,
            "objectCode": object_code,
            "name": "TestTable",
            "comment": "oh"
        }
        json_content = JSONRenderer().render(content)
        #print json_content
        data = {
            "content": json_content,
            "objectType": "Table",
            "objectCode": object_code,
            "changeType": 1,
            "isUIChange": True
        }
        change_creating_res = self.client.post(change_creating_url, data)
        self.assertEqual(change_creating_res.status_code, 200)

        saved_change = Change.objects.get(object_code=object_code)
        self.assertEqual(json_content, saved_change.content)
        self.assertEqual("Table", saved_change.object_type)
        self.assertEqual(1, saved_change.change_type)
        self.assertEqual(True, saved_change.is_ui_change)

        saved_assignment_entry = SandboxChange.objects.filter(sandbox_ref=sandbox, change_ref=saved_change).first()
        self.assertEqual(saved_change, saved_assignment_entry.change_ref)
        self.assertEqual(sandbox, saved_assignment_entry.sandbox_ref)

        #sandbox_url = "/api/sandboxes/1/"
        #sandbox_res = self.client.get(sandbox_url)
        #self.assertEqual(sandbox_res.status_code, 200)


    def test_serialization_util(self):
        t = Table()

        #JSONParser().parse(stream)


        ns = Namespace()
        ns.id = str(uuid4())
        ns.comment = "test"
        ns.abbreviation = "ASD"
        ns.name = "TEST"
        ns.schema_ref = str(uuid4())

        serializer = NamespaceSerializer(ns)
        json = JSONRenderer().render(serializer.data)
        c = Change()
        c.object_type = 'Namespace'
        c.content = json
        object = utils.change_to_object(c)

