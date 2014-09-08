import json
from uuid import uuid4
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from fennec.restapi.constants import MASTER_BRANCH_NAME, MASTER_BRANCH_DESCRIPTION, MASTER_BRANCH_TYPE
from fennec.restapi.versioncontroll.models import SandboxChange, Change, BranchRevisionChange

__author__ = 'Darko'


class DefaultAPITest(APITestCase):
    user = None

    def setUp(self):
        user = User.objects.create_superuser(email="test@test.com", username='test', password='test')
        self.client.force_authenticate(user=user)
        all_accounts = self.client.get("/api/users/")
        self.user_url = all_accounts.data[0]['url']
        self.user = user


class IntegrationTests(DefaultAPITest):
    def test_create_project(self):
        """
        Tests creation of Project as well as its main branch (as well as its zero revision), which is created automatically for each project
        """
        projects_url = "/api/projects/"
        data = {'id': 1, 'name': 'TestProject', 'description': 'This is a test', 'created_by': self.user.id}

        create_project_response = self.client.post(projects_url, data)
        self.assertEqual(create_project_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_project_response.data['id'], data['id'])
        self.assertEqual(create_project_response.data['name'], data['name'])
        self.assertEqual(create_project_response.data['description'], data['description'])
        self.assertEqual(create_project_response.data['created_by'], data['created_by'])

        branches_url = "/api/branches/"
        retrieve_branches_response = self.client.get(branches_url)
        self.assertEqual(retrieve_branches_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_branches_response.data[0]['project_ref'], data['id'])
        self.assertEqual(retrieve_branches_response.data[0]['name'], MASTER_BRANCH_NAME)
        self.assertEqual(retrieve_branches_response.data[0]['type'], MASTER_BRANCH_TYPE)
        self.assertEqual(retrieve_branches_response.data[0]['description'], MASTER_BRANCH_DESCRIPTION)

        branch_one_url = "/api/branches/1/"
        branch = self.client.get(branch_one_url)

        branch_revisions_url = "/api/branch-revisions/"
        retrieve_branch_revisions_response = self.client.get(branch_revisions_url)
        self.assertEqual(retrieve_branch_revisions_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_branch_revisions_response.data[0]['revision_number'], 0)
        self.assertEqual(retrieve_branch_revisions_response.data[0]['previous_revision_ref'], None)
        self.assertEqual(retrieve_branch_revisions_response.data[0]['branch_ref'], branch.data['id'])

    def test_branch_from_branch_revision(self):
        self.test_create_project()
        branch_revisions_url = "/api/branch-revisions/"
        branch_revision = self.client.get(branch_revisions_url).data[0]

        branch_from_branch_rev_url = "/api/branch-revisions/{}/branch/".format(branch_revision['id'])
        branching_request_data = {'name': 'develop', 'type': 'development', 'description': 'main development branch'}
        branch_from_branch_rev_response = self.client.post(branch_from_branch_rev_url, branching_request_data)
        self.assertEqual(branch_from_branch_rev_response.status_code, status.HTTP_201_CREATED)

        branches_ult = "/api/branches/"
        branches_response = self.client.get(branches_ult)

        self.assertEqual(2, len(branches_response.data))
        branches = branches_response.data
        new_branch = [x for x in branches if x['name'] == 'develop'][0]

        self.assertEqual(new_branch['type'], branching_request_data['type'])
        self.assertEqual(new_branch['description'], branching_request_data['description'])

    def test_post_changes_on_branch_revision(self):
        self.test_create_project()

        branch_revisions_url = "/api/branch-revisions/"
        branch_revision = self.client.get(branch_revisions_url).data[0]
        change_posting_url = "/api/branch-revisions/{}/change/".format(branch_revision['id'])
        example_diagram_data = {
            "id": str(uuid4()),
            "name": "TestDiagram",
            "description": "this is a diagram made for test"
        }
        example_diagram_string = json.dumps(example_diagram_data)
        change_data = {'content': example_diagram_string, 'objectType': 'Diagram',
                       'objectCode': example_diagram_data['id'],
                       'changeType': 0,
                       'isUIChange': True, 'made_by': self.user.id, '': '', }

        posting_response = self.client.post(change_posting_url, change_data)
        self.assertEqual(posting_response.status_code, status.HTTP_204_NO_CONTENT)

        # verify that change has been saved in database
        sandbox_changes = SandboxChange.objects.all()
        self.assertEqual(len(sandbox_changes), 1)
        changes = Change.objects.all()
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].content, change_data['content'])
        self.assertEqual(changes[0].object_type, change_data['objectType'])
        self.assertEqual(changes[0].change_type, change_data['changeType'])
        self.assertEqual(changes[0].object_code, change_data['objectCode'])
        self.assertEqual(changes[0].is_ui_change, change_data['isUIChange'])
        self.assertEqual(changes[0].made_by.id, change_data['made_by'])
        self.assertEqual(changes[0].content, change_data['content'])

    def test_commit_changes_on_branch_revision(self):
        """
        Commit change made in a previous test that is invoked at the start of the test.
        """
        self.test_post_changes_on_branch_revision()

        branch_rev_id = 1

        commit_url = "/api/branch-revisions/{}/commit/".format(branch_rev_id)

        commit_response = self.client.post(commit_url)
        self.assertEqual(commit_response.status_code, status.HTTP_200_OK)

        # verify that change has been saved as branch revision change
        branch_changes = BranchRevisionChange.objects.all()
        self.assertEqual(len(branch_changes), 1)

        # verify that old sandbox was closed

        # verify that new branch revision was created

    def test_commit_changes_on_separate_branch(self):
        self.test_create_project()

        branch_revisions_repsonse = self.client.get("/api/branch-revisions/")
        zero_revision = branch_revisions_repsonse.data[0]['id']

        # add diagram to zero revision
        diagram = {'id': str(uuid4()), 'name': 'MainDiagram'}
        diagram_add_change = {'content': json.dumps(diagram), 'objectType': 'Diagram', 'objectCode': str(uuid4()),
                              'changeType': 0,
                              'isUIChange': True, 'made_by': self.user.id}

        change_posting_url = "/api/branch-revisions/{}/change/".format(zero_revision)
        diagram_creation_response = self.client.post(change_posting_url, diagram_add_change)
        self.assertEqual(diagram_creation_response.status_code, status.HTTP_204_NO_CONTENT)

        # commit revision zero which contains only empty diagram

        initial_commit_url = "/api/branch-revisions/{}/commit/".format(zero_revision)
        initial_commit_response = self.client.post(initial_commit_url)
        self.assertEqual(initial_commit_response.status_code, status.HTTP_200_OK)

        # try to commit again zero revision and confirm it returns an error
        initial_commit_response = self.client.post(initial_commit_url)
        self.assertEqual(initial_commit_response.status_code, status.HTTP_400_BAD_REQUEST)

        # post a table and table symbol change on revision 1

        revision_two_url = "/api/branch-revisions/2/"

        # add schema

        schema = {'id': str(uuid4()), 'databaseName': 'default', 'collation': 'utf-8'}
        schema_add_change = {'content': json.dumps(schema), 'objectType': 'Schema', 'objectCode': schema['id'],
                             'changeType': 0,
                             'isUIChange': False, 'made_by': self.user.id}
        schema_creation_posting = self.client.post(revision_two_url + 'change/', schema_add_change)
        self.assertEqual(schema_creation_posting.status_code, status.HTTP_204_NO_CONTENT)

        # add table
        table = {'id': str(uuid4()), 'name': 'TableOne', 'collation': 'utf-8', 'comment': 'first table yay',
                 'schemaRef': schema['id'], }
        table_add_change = {'content': json.dumps(table), 'objectType': 'Table', 'objectCode': table['id'],
                            'changeType': 0,
                            'isUIChange': False, 'made_by': self.user.id}

        table_creation_posting = self.client.post(revision_two_url + 'change/', table_add_change)
        self.assertEqual(table_creation_posting.status_code, status.HTTP_204_NO_CONTENT)

        # add table symbol

        table_symbol = {'id': str(uuid4()), 'positionX': 12, 'positionY': 12, 'width': 50, 'height': 50,
                        'tableRef': table['id'], 'diagramRef': diagram['id'], 'color': '000000', 'collapsed': False}

        table_symbol_add_change = {'content': json.dumps(table_symbol), 'objectType': 'TableElement',
                                   'objectCode': table_symbol['id'],
                                   'changeType': 0,
                                   'isUIChange': True, 'made_by': self.user.id}

        table_creation_posting = self.client.post(revision_two_url + 'change/', table_symbol_add_change)
        self.assertEqual(table_creation_posting.status_code, status.HTTP_204_NO_CONTENT)


        # add namespace

        namespace = {'id': str(uuid4()), 'name': 'TestNamespace', 'comment': 'This is  a test namespace',
                     'abbreviation': 'TST', 'schemaRef': schema['id']}

        namespace_add_change = {'content': json.dumps(namespace), 'objectType': 'Namespace',
                                'objectCode': namespace['id'],
                                'changeType': 0,
                                'isUIChange': False, 'made_by': self.user.id}

        namespace_creation_posting = self.client.post(revision_two_url + 'change/', namespace_add_change)
        self.assertEqual(namespace_creation_posting.status_code, status.HTTP_204_NO_CONTENT)

        second_commit_response = self.client.post(revision_two_url + 'commit/')
        self.assertEqual(second_commit_response.status_code, status.HTTP_200_OK)

        # retrieval of metadata and symbol data to verify that it was really created

        metadata_retrieval_result = self.client.get(revision_two_url + 'metadata/')
        self.assertEqual(metadata_retrieval_result.status_code, status.HTTP_200_OK)
        self.assertEqual(len(metadata_retrieval_result.data), 1)
        retrieved_schema = metadata_retrieval_result.data[0]
        self.assertEqual(retrieved_schema['id'], schema['id'])
        self.assertEqual(retrieved_schema['databaseName'], schema['databaseName'])
        self.assertEqual(retrieved_schema['collation'], schema['collation'])

        self.assertEqual(len(retrieved_schema['tables']), 1)
        retrieved_table = retrieved_schema['tables'][0]
        self.assertEqual(retrieved_table['id'], table['id'])
        self.assertEqual(retrieved_table['name'], table['name'])
        self.assertEqual(retrieved_table['collation'], table['collation'])
        self.assertEqual(retrieved_table['comment'], table['comment'])
        self.assertEqual(retrieved_table['schemaRef'], table['schemaRef'])

        self.assertEqual(len(retrieved_schema['namespaces']), 1)
        retrieved_namespace = retrieved_schema['namespaces'][0]
        self.assertEqual(retrieved_namespace['id'], namespace['id'])
        self.assertEqual(retrieved_namespace['name'], namespace['name'])
        self.assertEqual(retrieved_namespace['comment'], namespace['comment'])
        self.assertEqual(retrieved_namespace['abbreviation'], namespace['abbreviation'])
        self.assertEqual(retrieved_namespace['schemaRef'], namespace['schemaRef'])


        # retrieval of symbol data

        diagram_retrieval_result = self.client.post(revision_two_url + 'diagram/?diagramId=' + diagram['id'])
        self.assertEqual(diagram_retrieval_result.status_code, status.HTTP_200_OK)
        diagram = diagram_retrieval_result.data
        self.assertEqual(diagram['id'], diagram['id'])
        self.assertEqual(diagram['name'], diagram['name'])
        self.assertEqual(diagram['description'], diagram['description'])
        self.assertEqual(len(diagram['tableElements']), 1)
        self.assertEqual(diagram['tableElements'][0]['id'], table_symbol['id'])
        self.assertEqual(diagram['tableElements'][0]['positionX'], table_symbol['positionX'])
        self.assertEqual(diagram['tableElements'][0]['positionY'], table_symbol['positionY'])
        self.assertEqual(diagram['tableElements'][0]['width'], table_symbol['width'])
        self.assertEqual(diagram['tableElements'][0]['height'], table_symbol['height'])
        self.assertEqual(diagram['tableElements'][0]['tableRef'], table_symbol['tableRef'])
        self.assertEqual(diagram['tableElements'][0]['color'], table_symbol['color'])
        self.assertEqual(diagram['tableElements'][0]['collapsed'], table_symbol['collapsed'])

        # retrieval of project state

        project_current_state_url = revision_two_url + 'project_state/'
        project_current_state = self.client.get(project_current_state_url)
        self.assertEqual(project_current_state.status_code, status.HTTP_200_OK)

        revision_three_url = "/api/branch-revisions/3/"

        altered_table = {'id': table['id'], 'name': 'TableOneTwo', 'collation': 'utf-8', 'comment': 'first table yay',
                         'schemaRef': schema['id'], }
        table_alter_change = {'content': json.dumps(altered_table), 'objectType': 'Table', 'objectCode': altered_table['id'],
                              'changeType': 1,
                              'isUIChange': False, 'made_by': self.user.id}
        table_alternation_posting = self.client.post(revision_three_url + 'change/', table_alter_change)
        self.assertEqual(table_alternation_posting.status_code, status.HTTP_204_NO_CONTENT)

        project_current_state_url = revision_three_url + 'project_state/'
        project_current_state = self.client.get(project_current_state_url)
        self.assertEqual(project_current_state.status_code, status.HTTP_200_OK)
        schemas = project_current_state.data['schemas']
        self.assertEqual(len(schemas), 1)
        retrieved_schema = schemas[0]
        self.assertEqual(retrieved_schema['id'], schema['id'])
        self.assertEqual(retrieved_schema['databaseName'], schema['databaseName'])
        self.assertEqual(retrieved_schema['collation'], schema['collation'])

        self.assertEqual(len(retrieved_schema['tables']), 1)
        retrieved_table = retrieved_schema['tables'][0]
        self.assertEqual(retrieved_table['id'], altered_table['id'])
        self.assertEqual(retrieved_table['name'], altered_table['name'])
        self.assertEqual(retrieved_table['collation'], altered_table['collation'])
        self.assertEqual(retrieved_table['comment'], altered_table['comment'])
        self.assertEqual(retrieved_table['schemaRef'], altered_table['schemaRef'])


