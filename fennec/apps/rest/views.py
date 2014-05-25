from django.contrib.auth.models import User, Group
from models import Project, Branch
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, ProjectSerializer, BranchSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def pre_save(self, obj, created=False):
        print 'sup'


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    @api_view(['GET'])
    def hello_world(request):
        return Response({"message":"hello"})