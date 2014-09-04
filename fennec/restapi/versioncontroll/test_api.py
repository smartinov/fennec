from django.contrib.auth.models import User
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase
from fennec.restapi.constants import MASTER_BRANCH_NAME, MASTER_BRANCH_DESCRIPTION, MASTER_BRANCH_TYPE

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
        Tests creation of Project as well as its main branch, which is created automatically for each project
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