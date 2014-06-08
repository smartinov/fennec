from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, link
from django.contrib.auth.models import User, Group
from models import Project, Branch, Change
from serializers import ProjectSerializer, BranchSerializer, GroupSerializer, UserSerializer, ChangeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class ChangeViewSet(viewsets.ModelViewSet):
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer

    @link()
    def get_all(self, request, pk=None):
        return Response({'test': "test"})

    @action(methods=['post'])
    def post_some(self):
        return Response({'test': "test"})

class TestViewSet(viewsets.ViewSet):

    @link()
    def get_all(self):
        return Response({'test': "test"})

    @action(methods=['post'])
    def post_some(self):
        return Response({'test': "test"})
