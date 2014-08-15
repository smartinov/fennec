from StringIO import StringIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from fennec.restapi.dbmodel.models import Table, Column, Index, RelationshipElement, TableElement, Layer, Diagram, ForeignKey, Schema, Namespace
from fennec.restapi.dbmodel.serializers import SchemaSerializer, NamespaceSerializer, TableSerializer, ColumnSerializer, IndexSerializer, ForeignKeySerializer, LayerSerializer, TableElementSerializer, RelationshipElementSerializer, DiagramSerializer
from fennec.restapi.versioncontroll.models import Sandbox, Branch, BranchRevision, SANDBOX_STATUS, SandboxChange, BranchRevisionChange, Change

__author__ = 'Darko'


def change_to_object(change):
    """
    change is Change
    """
    stream = StringIO(change.content)
    data = JSONParser().parse(stream)
    serializer = swithc_type(change.change_type)(data=data)
    return serializer.object

def swithc_type(object_type):
    
    return {
        'Schema': SchemaSerializer,
        'Namespace': NamespaceSerializer,
        'Table': TableSerializer,
        'Column': ColumnSerializer,
        'Index': IndexSerializer,
        'ForeignKey': ForeignKeySerializer,
        'Diagram': DiagramSerializer,
        'Layer': LayerSerializer,
        'TableElement': TableElementSerializer,
        'RelationshipElement': RelationshipElementSerializer
    }.get(object_type, None)


class BranchRevisionState(object):
    branch_rev_id = ''

    def __init__(self, branch_rev_id):
        self.branch_rev_id = branch_rev_id

    def get_state(self):
        changes = BranchRevisionChange


class SandboxState(object):
    user = ''
    branch_id = ''

    def __init__(self, user, branch_id):
        self.branch_id = branch_id
        self.user = user

    def get_state(self):



        sandbox = obtain_sandbox(self.user, self.branch_id)

        sandbox_changes = SandboxChange.objects.filter(sandbox_ref=sandbox).order_by('ordinal')


        pass


def changes_to_objects(changes):
    objects = []
    for change in changes:
        print change


def obtain_sandbox(user, branch_id):
    branch = Branch.objects.get(pk=int(branch_id))
    sandbox = Sandbox.objects.filter(bound_to_branch_ref=branch, created_by__id=user.id, status=0, is_deleted=False).first()
    if sandbox is None:
        branch_revision = BranchRevision.objects.filter(branch_ref=branch).order_by('revision_number').last()

        sandbox = Sandbox()
        sandbox.created_by = user
        sandbox.bound_to_branch_ref = branch
        sandbox.created_from_branch_revision_ref = branch_revision
        sandbox.status = 0
        sandbox.is_deleted = False
        sandbox.save()
    return sandbox
