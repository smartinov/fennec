from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, link, api_view
from django.contrib.auth.models import User, Group
from fennec.restapi.constants import MASTER_BRANCH_NAME, MASTER_BRANCH_TYPE, MASTER_BRANCH_DESCRIPTION
from fennec.restapi.dbmodel.serializers import SchemaSerializer, DiagramSerializer, SandboxBasicInfoSerializer
from fennec.restapi.versioncontroll import utils
from fennec.restapi.versioncontroll.models import Project, Branch, BranchRevision, SandboxChange
from fennec.restapi.versioncontroll.serializers import BranchRevisionSerializer, ChangeSerializer
from fennec.restapi.versioncontroll.utils import SandboxState
from serializers import ProjectSerializer, BranchSerializer, GroupSerializer, UserSerializer


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

    # def list(self, request, project_id_id=None, *args, **kwargs):
    # #id_id <- w/e it works!
    # #print kwargs
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

    @action(methods=['GET'])
    def sandbox(self, request, id=None, project_id_id=None):
        result = {"test": "123"}
        sandbox_state = SandboxState
        return Response(result, status=status.HTTP_200_OK)


class BranchRevisionViewSet(viewsets.ModelViewSet):
    queryset = BranchRevision.objects.all()
    serializer_class = BranchRevisionSerializer
    lookup_field = 'id'

    # def list(self, request, branch_id_id=None, *args, **kwargs):
    # #id_id <- w/e it works!
    # #print kwargs
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

    @action(methods=['POST'])
    def change(self, request, id=None):
        #print request.DATA
        serializer = ChangeSerializer(data=request.DATA)
        #print serializer.is_valid()
        #print serializer.object
        #print serializer.errors
        if serializer.is_valid():
            branch_rev = BranchRevision.objects.filter(id=id).first()
            sandbox = utils.obtain_sandbox(request.user, branch_rev.branch_ref.id)
            if sandbox.status != 0:
                return Response(error="cannot commit a closed sandbox", status=status.HTTP_400_BAD_REQUEST)

            change = serializer.object
            change.made_by = request.user
            change.save()
            sandbox_change = SandboxChange()
            sandbox_change.change_ref = change
            sandbox_change.ordinal = SandboxChange.objects.filter(change_ref=change).count() + 1
            sandbox_change.sandbox_ref = sandbox
            sandbox_change.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            print "\nerrors occured:\n"
            print serializer.errors
        return Response("error occured", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action()
    def commit(self, request, id=None):
        branch_revision = self.get_object()
        latest_branch_revision = BranchRevision.objects.filter(branch_ref=branch_revision.branch_ref).order_by(
            '-revision_number').first()
        if branch_revision.id != latest_branch_revision.id:
            return Response("cannot commit a on branch revision that is not latest!",
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        sandbox = utils.obtain_sandbox(user, branch_revision.branch_ref.id)
        if sandbox.status != 0:
            return Response("cannot commit a closed sandbox", status=status.HTTP_400_BAD_REQUEST)
        utils.commit_sandbox(sandbox, request.user)
        return Response(status=status.HTTP_200_OK)


    @link()
    def project_state(self, request, id=None):
        branch_revision = self.get_object()
        user = request.user
        sandbox = utils.obtain_sandbox(user, branch_revision.branch_ref.id)

        sandbox_state = SandboxState(user, sandbox)
        sandbox_state.build_sandbox_state_metadata()
        sandbox_state.build_sandbox_state_symbols()

        sandbox_info = sandbox_state.build_project_info()
        serializer = SandboxBasicInfoSerializer(sandbox_info)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @link()
    def metadata(self, request, id=None):
        branch_revision = self.get_object()
        user = request.user
        sandbox = utils.obtain_sandbox(user, branch_revision.branch_ref.id)

        sandbox_state = SandboxState(user, sandbox)
        sandbox_state.build_sandbox_state_metadata()
        schemas = sandbox_state.schemas
        serializer = SchemaSerializer(schemas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action()
    def diagram(self, request, id=None):
        branch_revision = self.get_object()
        user = request.user
        sandbox = utils.obtain_sandbox(user, branch_revision.branch_ref.id)

        sandbox_state = SandboxState(user, sandbox)
        sandbox_state.build_sandbox_state_symbols()
        diagram = sandbox_state.retrieve_diagram_details(request.QUERY_PARAMS.get('diagramId', None))

        serializer = DiagramSerializer(diagram, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)