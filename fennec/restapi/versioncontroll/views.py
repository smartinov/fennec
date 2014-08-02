import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, link
from django.contrib.auth.models import User, Group
from fennec.restapi.dbmodel.addins import changes
from fennec.restapi.dbmodel.models import Project, Branch, Change, Sandbox
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

    @action()
    def commit(self, request, pk):
        branch = self.get_object()
        user = request.user
        sandbox = Sandbox.obtain_sandbox(user, branch.id)
        rez = sandbox.collect_changes()
        print rez


class ChangeViewSet(viewsets.ModelViewSet):
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer

    @link()
    def get_all(self, request, pk=None):
        return Response({'test': "test"})

    @action(methods=['post'])
    def post_some(self):
        return Response({'test': "test"})


    @action(methods=['post'])
    def persist_changes(self):
        user = self.request.user
        branch_id = self.request.DATA['branch_id']
        sandbox = Sandbox.obtain_sandbox(user, branch_id)
        changes.len()
        #cset = ChangeSet()
        #cset.comment = self.request.DATA['comment']
        #cset.submitted_by = user
        #cset.submitted_on = datetime.datetime.now()
        ##cset.branch_revision_ref =
        #cset.save()
        #
        #for change in changes:
        #    change.change_set_ref = cset
        #    change.ordinal = changes.index(change)
        #    change.save()


class TestViewSet(viewsets.ViewSet):

    @link()
    def get_all(self):
        return Response({'test': "test"})

    @action(methods=['post'])
    def post_some(self):
        return Response({'test': "test"})
