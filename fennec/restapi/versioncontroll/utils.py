from StringIO import StringIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from south.creator.freezer import model_dependencies
from fennec.restapi.dbmodel.models import Table, Column, Index, RelationshipElement, TableElement, Layer, Diagram, ForeignKey, Schema, Namespace
from fennec.restapi.dbmodel.serializers import SchemaSerializer, NamespaceSerializer, TableSerializer, ColumnSerializer, IndexSerializer, ForeignKeySerializer, LayerSerializer, TableElementSerializer, RelationshipElementSerializer, DiagramSerializer
from fennec.restapi.versioncontroll.models import Sandbox, Branch, BranchRevision, SANDBOX_STATUS, SandboxChange, BranchRevisionChange, Change, CHANGE_TYPE

__author__ = 'Darko'


def change_to_object(change):
    """
    change is Change
    """
    stream = StringIO(change.content)
    data = JSONParser().parse(stream)
    serializer = swithc_type(change.object_type)(data=data)
    if not serializer.is_valid():
        raise Exception(serializer.errors)

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

    def get_revision_cumulative_changes(self):
        model_changes = {}
        symbol_changes = {}

        #get previous revision changes:
        branch_rev = BranchRevision.objects.get(id=self.branch_rev_id)
        previous_branch_revs = BranchRevision.objects.filter(branch_ref=branch_rev.branch_ref,
                                                             revision_number__lte=branch_rev.revision_number).order_by(
            'revision_number').all()
        for prev_rev in previous_branch_revs:
            branch_rev_changes = BranchRevisionChange.objects.filter(branch_revision_ref=prev_rev).order_by(
                'ordinal').all()
            for branch_rev_change in branch_rev_changes:
                change = Change.objects.get(id=branch_rev_change.change_ref.id)

                if change.is_ui_change:
                    if change.change_type == 2:
                        del symbol_changes[change.object_code]
                    else:
                        symbol_changes[change.object_code] = change
                else:
                    if change.change_type == 2:
                        del model_changes[change.object_code]
                    else:
                        model_changes[change.object_code] = change
        return model_changes, symbol_changes

    def build_state_metadata(self):
        model_changes, symbol_changes = self.get_revision_cumulative_changes()

        schemas = []
        return build_state_metadata(schemas, model_changes.values())

    def build_state_symbols(self):
        model_changes, symbol_changes = self.get_revision_cumulative_changes()
        diagrams = []
        return build_state_symbols(diagrams, symbol_changes.values())


def build_state_metadata(schemas, new_changes):
    """
    schemas is array of Schema 's representing current state
    new_changes are Change objects that need to be applied to current state
    """
    model_objects = []

    for model_change in new_changes:
        model_objects.append(change_to_object(model_change))

    schemas = [x for x in model_objects if isinstance(x, Schema)]
    namespaces = [x for x in model_objects if isinstance(x, Namespace)]
    tables = [x for x in model_objects if isinstance(x, Table)]
    columns = [x for x in model_objects if isinstance(x, Column)]
    indexes = [x for x in model_objects if isinstance(x, Index)]
    foreign_keys = [x for x in model_objects if isinstance(x, ForeignKey)]
    for schema in schemas:
        schema.namespaces = []
        schema.tables = []

        schema.namespaces = [x for x in namespaces if x.schema_ref == schema.id]

        schema_tables = [x for x in tables if x.schema_ref == schema.id]

        for sch_table in schema_tables:
            sch_table.columns = [x for x in columns if x.table_ref == sch_table.id]
            sch_table.indexes = [x for x in indexes if x.table_ref == sch_table.id]
            sch_table.foreign_keys = [x for x in foreign_keys if x.table_ref == sch_table.id]
            schema.tables.append(sch_table)
    return schemas


def build_state_symbols(schemas, new_changes):
    symbol_objects = []
    for symbol_change in new_changes:
        symbol_objects.append(change_to_object(symbol_change))

    diagrams = [x for x in symbol_objects if isinstance(x, Diagram)]
    layers = [x for x in symbol_objects if isinstance(x, Layer)]
    table_elements = [x for x in symbol_objects if isinstance(x, TableElement)]
    relationship_element = [x for x in symbol_objects if isinstance(x, RelationshipElement)]

    for diagram in diagrams:
        diagram.layers = []
        diagram.table_elements = []
        diagram.relationship_elements = []

        dia_layers = [x for x in layers if x.diagram_ref == diagram.id]
        dia_tables = [x for x in table_elements if x.diagram_ref == diagram.id]
        dia_relationships = [x for x in relationship_element if x.diagram_ref == diagram.id]
        diagram.layers = dia_layers
        diagram.table_elements = dia_tables
        diagram.relationship_elements = dia_relationships
    return diagrams


def obtain_sandbox(user, branch_id):
    branch = Branch.objects.get(pk=int(branch_id))
    sandbox = Sandbox.objects.filter(bound_to_branch_ref=branch, created_by__id=user.id, status=0,
                                     is_deleted=False).first()
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

    def build_sandbox_state_metadata(self):
        last_branch_revision = BranchRevision.objects.filter(branch_ref=self.branch_id) \
            .order_by(-'revision_number').first()


        sandbox = obtain_sandbox(self.user, self.branch_id)
        #if sanadbox. is behind top branch revision throw exception for now
        if not sandbox.created_from_branch_revision_ref.id == last_branch_revision.id:
            raise Exception("Invalid stuff")

        branch_rev_state = BranchRevisionState(last_branch_revision.id)
        schemas = branch_rev_state.build_state_metadata()

        sandbox_changes = SandboxChange.objects.filter(sandbox_ref=sandbox)

        schemas = build_state_metadata(schemas, sandbox_changes)
        return schemas

    def build_sandbox_state_symbols(self):
        last_branch_revision = BranchRevision.objects.filter(branch_ref=self.branch_id) \
            .order_by(-'revision_number').first()


        sandbox = obtain_sandbox(self.user, self.branch_id)
        #if sanadbox. is behind top branch revision throw exception for now
        if not sandbox.created_from_branch_revision_ref.id == last_branch_revision.id:
            raise Exception("Invalid stuff")

        branch_rev_state = BranchRevisionState(last_branch_revision.id)
        diagrams = branch_rev_state.build_state_symbols()

        sandbox_changes = SandboxChange.objects.filter(sandbox_ref=sandbox)

        diagrams = build_state_symbols(diagrams, sandbox_changes)
        return diagrams
