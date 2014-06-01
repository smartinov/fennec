from rest_framework import viewsets
from django.contrib.auth.models import User, Group

from models import Project, Branch
from serializers import ProjectSerializer, BranchSerializer, GroupSerializer, UserSerializer
from fennec.restapi.notifications.models import Notification


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post_save(self, obj, created):
        notif = Notification()
        notif.recipient = self.request.user
        notif.content = "{0} {1} the project {2}".format(
            self.request.user.username,
            "created" if created else "edited",
            obj.name)
        notif.save()


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
