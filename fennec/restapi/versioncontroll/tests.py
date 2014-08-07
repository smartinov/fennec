from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
from fennec.restapi.dbmodel.models import Project, Branch
from fennec.restapi.versioncontroll.views import ProjectViewSet


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
        self.assertEqual(p2_branches_response.data[2]['project_ref'], project_two.id)
