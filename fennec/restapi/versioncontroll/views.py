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
        content = "{0} just {1} the project {2}".format(
            self.request.user.username,
            "created" if created else "edited",
            obj.name)
        notif = self._get_notification(content)
        notif.save()

    def post_delete(self, obj):
        content = "{0} just deleted the project {1}".format(
            self.request.user.username,
            obj.name)
        notif = self._get_notification(content)
        notif.save()

    def _get_notification(self, text):
        notif = Notification()
        notif.created_by = self.request.user
        notif.source = "projects"
        notif.recipient = self.request.user
        notif.content = text
        return notif


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
