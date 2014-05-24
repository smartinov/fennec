from django.contrib.auth.models import User, Group
from models import Project
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, ProjectSerializer


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