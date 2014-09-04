from django.http import response
from rest_framework import viewsets, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, link, api_view
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from fennec.restapi.constants import MASTER_BRANCH_NAME, MASTER_BRANCH_TYPE, MASTER_BRANCH_DESCRIPTION
from fennec.restapi.versioncontroll.addins import changes
from fennec.restapi.versioncontroll.models import Project, Branch, Change, Sandbox, BranchRevision, SandboxChange
from fennec.restapi.versioncontroll.serializers import BranchRevisionSerializer, SandboxSerializer
from fennec.restapi.versioncontroll.utils import SandboxState
from serializers import ProjectSerializer, BranchSerializer, GroupSerializer, UserSerializer, ChangeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'

    def post_save(self, obj, created=False):
        if created:
            branch = Branch(created_by=obj.created_by, current_version=0, description=MASTER_BRANCH_DESCRIPTION,
                            name=MASTER_BRANCH_NAME, project_ref=obj, type=MASTER_BRANCH_TYPE)
            branch.save()
            revision_zero = BranchRevision(revision_number=0, branch_ref=branch)
            revision_zero.save()


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'id'

    def post_save(self, obj, created=False):
        if created:
            revision_zero = BranchRevision(revision_number=0, branch_ref=obj)
            revision_zero.save()

    #def list(self, request, project_id_id=None, *args, **kwargs):
    #    #id_id <- w/e it works!
    #    #print kwargs
    #    queryset = self.queryset.filter(project_ref=project_id_id)
    #    serializer = BranchSerializer(queryset, many=True)
    #    return Response(serializer.data)
    #
    #def create(self, request, project_id_id=None, *args, **kwargs):
    #    serializer = self.get_serializer(data=request.DATA, files=request.FILES)
    #
    #    if serializer.is_valid():
    #        serializer.object.project_ref = Project.objects.filter(id=project_id_id).first()
    #        self.pre_save(serializer.object)
    #        self.object = serializer.save(force_insert=True)
    #        self.post_save(self.object, created=True)
    #        headers = self.get_success_headers(serializer.data)
    #        return Response(serializer.data, status=status.HTTP_201_CREATED,
    #                        headers=headers)
    #
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action()
    def commit(self, request, pk):
        branch = self.get_object()
        user = request.user
        sandbox = Sandbox.obtain_sandbox(user, branch.id)
        rez = sandbox.collect_changes()
        #print rez


    @action(methods=['GET'])
    def sandbox(self, request, id=None, project_id_id=None):
        print "id: {}  project_id: {}".format(id, project_id_id)
        result = {"test": "123"}
        sandbox_state = SandboxState
        return Response(result, status=status.HTTP_200_OK)


class BranchRevisionViewSet(viewsets.ModelViewSet):
    queryset = BranchRevision.objects.all()
    serializer_class = BranchRevisionSerializer
    lookup_field = 'id'

    #def list(self, request, branch_id_id=None, *args, **kwargs):
    #    #id_id <- w/e it works!
    #    #print kwargs
    #    queryset = self.queryset.filter(branch_ref=branch_id_id)
    #    serializer = BranchRevisionSerializer(queryset, many=True)
    #    return Response(serializer.data)


    @action()
    def branch(self, request, id=None, project_id_id=None, ):
        branch_rev = BranchRevision.objects.filter(id=id).first()
        name = request.DATA['name']
        type = request.DATA['type']
        description = request.DATA['description']
        new_branch = Branch(name=name, description=description, type=type, created_by=request.user,
                            project_ref=branch_rev.branch_ref.project_ref, parent_branch_revision=branch_rev)
        new_branch.save()
        return Response(status=status.HTTP_201_CREATED)


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


changes = []


class SandboxView(viewsets.ViewSet):
    model = Sandbox
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.AllowAny,)

    def list(self, request):
        queryset = Sandbox.objects.all()
        serializer = SandboxSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Sandbox.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = SandboxSerializer(user)
        return Response(serializer.data)

    @action(methods=['GET'])
    def test(self, request, pk=None, format=None):
        #print pk
        return Response({'test': "test"})

    @action(methods=['POST'])
    def change(self, request, pk=None, format=None):
        #print request.DATA
        serializer = ChangeSerializer(data=request.DATA)
        #print serializer.is_valid()
        #print serializer.object
        #print serializer.errors
        if serializer.is_valid():
            change = serializer.object
            change.made_by = request.user
            change.save()
            sandbox_change = SandboxChange()
            sandbox_change.change_ref = change
            sandbox_change.ordinal = SandboxChange.objects.filter(change_ref=change).count() + 1
            sandbox_change.sandbox_ref = Sandbox.objects.get(id=pk)
            sandbox_change.save()
            changes.append(change)
            return Response(status.HTTP_200_OK)
        return Response("error occured", status.HTTP_500_INTERNAL_SERVER_ERROR)


        #
        #@action(methods=['POST'])
        #def test(self):
        #    return Response({'test': "test"})

        #def get(self, request, project_id, branch_id, *args, **kwargs):
        #    #retrieve user
        #    #retrieve branch
        #    #retrieve sandbox based on that
        #
        #    sbstate = SandboxState()
        #    state = sbstate.get_state()
        #    response = Response(state, status=status.HTTP_200_OK)
        #    return response