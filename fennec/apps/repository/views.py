from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action, link
from django.contrib.auth.models import User, Group

from fennec.apps.constants import MASTER_BRANCH_NAME, MASTER_BRANCH_TYPE, MASTER_BRANCH_DESCRIPTION
from fennec.apps.metamodel.serializers import SchemaSerializer, DiagramSerializer, SandboxBasicInfoSerializer, \
    ChangeSerializer
from fennec.apps.repository import utils
from fennec.apps.repository.models import Project, ProjectMember, Branch, BranchRevision, SandboxChange
from fennec.apps.repository.serializers import BranchRevisionSerializer
from fennec.apps.repository.utils import SandboxState
from fennec.apps.repository.serializers import ProjectSerializer, ProjectMemberSerializer, BranchSerializer, GroupSerializer, UserSerializer


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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('created_by',)

    def post_save(self, obj, created=False):
        """
        After saving of new project create new 'master' branch and its zero revision.
        """
        if created:
            branch = Branch(created_by=obj.created_by, current_version=0, description=MASTER_BRANCH_DESCRIPTION,
                            name=MASTER_BRANCH_NAME, project_ref=obj, type=MASTER_BRANCH_TYPE)
            branch.save()
            revision_zero = BranchRevision(revision_number=0, branch_ref=branch)
            revision_zero.save()


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    lookup_field = 'id'


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'id'
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project_ref',)

    def post_save(self, obj, created=False):
        """
        After saving of new branch create zero revision for it.
        """
        if created:
            revision_zero = BranchRevision(revision_number=0, branch_ref=obj)
            revision_zero.save()

    @action(methods=['GET'])
    def sandbox(self, request, id=None, project_id_id=None):
        result = {"test": "123"}
        sandbox_state = SandboxState
        return Response(result, status=status.HTTP_200_OK)


class BranchRevisionViewSet(viewsets.ModelViewSet):
    queryset = BranchRevision.objects.all()
    serializer_class = BranchRevisionSerializer
    lookup_field = 'id'
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('branch_ref',)

    @action()
    def branch(self, request, id=None, project_id_id=None, ):
        """
        Branch from current branch.
        """
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
        """
        Persists a change for given branch revision.
        Change is persisted as sandbox change.
        """
        serializer = ChangeSerializer(data=request.DATA)
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
        """
        Commits current sandbox changes. See 'utils.commit_sandbox'
        """
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
        """
        Builds and returns full sandbox state. Contains both metadata and symbols (diagrams)
        """
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
        """
        Builds and returns sandbox metadata.
        """
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
        """
        Builds and returns single diagram.
        """
        branch_revision = self.get_object()
        user = request.user
        sandbox = utils.obtain_sandbox(user, branch_revision.branch_ref.id)

        sandbox_state = SandboxState(user, sandbox)
        sandbox_state.build_sandbox_state_symbols()
        diagram = sandbox_state.retrieve_diagram_details(request.QUERY_PARAMS.get('diagramId', None))

        serializer = DiagramSerializer(diagram)
        return Response(serializer.data, status=status.HTTP_200_OK)