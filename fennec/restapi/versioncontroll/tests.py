from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
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
        Ensure we can create a new project
        """
        url = "/api/projects/"
        data = {'id': 1, 'name': 'TestProject', 'description': 'This is a test', 'created_by': self.user_url}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], data['id'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['created_by'], data['created_by'])
