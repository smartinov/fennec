from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
from fennec.restapi.versioncontroll.views import ProjectViewSet


class ProjectTests(APITestCase):
    def test_create_project(self):
        """
        Ensure we can create a new project
        """



        user = User.objects.create_user(username='test', password='test')
        resp = self.client.login(username='test', password='test')
        print 'login response:{}'.format(resp)
        print Token.objects.get(user_id = user.pk)
        client = APIClient()
        client.force_authenticate(user=user)


        get_all_projects = self.client.get("/api/projects/")
        print get_all_projects.status_code
        print get_all_projects.data

        url = "/api/projects/"
        data = {'id': 1, 'name': 'TestProject', 'description': 'This is a test', 'created_by': 1}
        response = client.post(url, data, format='json')

        print "content:"
        print response.content
        print "\n\n\n"
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        get_all_tests = self.client.get(url, format='josn')
        print get_all_tests