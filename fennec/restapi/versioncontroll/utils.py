from StringIO import StringIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from south.creator.freezer import model_dependencies
from fennec.restapi.dbmodel.models import Table, Column, Index, RelationshipElement, TableElement, Layer, Diagram, \
    ForeignKey, Schema, Namespace
from fennec.restapi.dbmodel.serializers import SchemaSerializer, NamespaceSerializer, TableSerializer, ColumnSerializer, \
    IndexSerializer, ForeignKeySerializer, LayerSerializer, TableElementSerializer, RelationshipElementSerializer, \
    DiagramSerializer
from fennec.restapi.versioncontroll.models import Sandbox, Branch, BranchRevision, SANDBOX_STATUS, SandboxChange, \
    BranchRevisionChange, Change, CHANGE_TYPE

__author__ = 'Darko'


def change_to_object(change):
    """
    change is Change
    """
    stream = StringIO(change.content)
    data = JSONParser().parse(stream)
    serializer = switch_type(change.object_type)(data=data)
    if not serializer.is_valid():
        raise Exception(serializer.errors)

    return serializer.object


def switch_type(object_type):
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


def branch_from_branch_revision(branch_rev, account, name, type=None,
                                description=None):
    """
    @type branch_rev: BranchRevision
    """
    new_branch = Branch(name=name, type=type, description=description,
                        project_ref=branch_rev.branch_ref.project_ref, created_by=account,
                        parent_branch_revision=branch_rev, current_version=0)
    new_branch.save()
    new_branch_zero_rev = BranchRevision(revision_number=0, branch_ref=new_branch)
    new_branch_zero_rev.save()
    return new_branch


def commit_sandbox(sandbox, user):
    """
    @type sandbox Sandbox
    """
    if sandbox.created_by != user:
        raise 'Woops'

    if check_for_conflicts():
        # TODO: Resolve conflicts
        pass

    original_branch_rev = sandbox.created_from_branch_revision_ref

    last_branch_revision = BranchRevision.objects.filter(branch_ref=sandbox.bound_to_branch_ref).order_by(
        -'revision_number').first()

    new_branch_revision = BranchRevision(revision_number=last_branch_revision.revision_number + 1,
                                         previous_revision_ref=last_branch_revision,
                                         branch_rev=last_branch_revision.branch_rev)
    new_branch_revision.save()

    original_branch = new_branch_revision.branch_ref
    original_branch.current_version = new_branch_revision.revision_number
    original_branch.save()

    __bind_sandbox_changes_to_branch_revision__(sandbox, new_branch_revision)

    sandbox.status = SANDBOX_STATUS.CLOSED
    sandbox.save()


def __bind_sandbox_changes_to_branch_revision__(sandbox, branch_revision):
    sandbox_changes = SandboxChange.objects.filter(sandbox_ref=sandbox).all()
    for i, sandbox_change in enumerate(sandbox_changes):
        branch_rev_change = BranchRevisionChange()
        branch_rev_change.branch_revision_ref = branch_revision
        branch_rev_change.change_ref = sandbox_change.change_ref
        branch_rev_change.ordinal = sandbox_change.ordinal
        branch_rev_change.save()


def check_for_conflicts():
    pass


class BranchRevisionState(object):
    branch_rev = None

    def __init__(self, branch_rev):
        self.branch_rev = branch_rev


    def __get_previous_revisions_from_all_branches__(self):
        """
        @type last_branch_rev BranchRevision
        """
        previous_revisions = []
        previous_revisions.append(self.branch_rev)
        last_branch_rev = self.branch_rev.previous_revision_ref
        while last_branch_rev is not None:
            previous_revisions.append(last_branch_rev)
            last_branch_rev = last_branch_rev.previous_revision_ref

        return reversed(previous_revisions)

    def get_revision_cumulative_changes(self):
        model_changes = {}
        symbol_changes = {}

        previous_branch_revs = self.__get_previous_revisions_from_all_branches__()
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


class SandboxState(object):
    user = None
    sandbox = None
    model_changes = {}
    symbol_changes = {}

    def __init__(self, user, sandbox):
        self.user = user
        self.sandbox = sandbox

    def populate_changes(self):
        sandbox_changes = SandboxChange.objects.filter(sandbox_ref=self.sandbox)

        for sandbox_change in sandbox_changes:
            change = Change.objects.get(id=sandbox_change.change_ref.id)

            if change.is_ui_change:
                if change.change_type == 2:
                    del self.symbol_changes[change.object_code]
                else:
                    self.symbol_changes[change.object_code] = change
            else:
                if change.change_type == 2:
                    del self.model_changes[change.object_code]
                else:
                    self.model_changes[change.object_code] = change

    def build_sandbox_state_metadata(self):
        # last_branch_revision = BranchRevision.objects.filter(branch_ref=self.branch_id) \
        # .order_by(-'revision_number').first()

        branch_rev_state = BranchRevisionState(self.sandbox.created_from_branch_revision_ref)
        schemas = branch_rev_state.build_state_metadata()
        self.populate_changes()
        schemas = build_state_metadata(schemas, self.model_changes.values())
        return schemas

    def build_sandbox_state_symbols(self):
        # last_branch_revision = BranchRevision.objects.filter(branch_ref=self.branch_id) \
        # .order_by(-'revision_number').first()

        branch_rev_state = BranchRevisionState(self.sandbox.created_from_branch_revision_ref)
        diagrams = branch_rev_state.build_state_symbols()
        self.populate_changes()
        diagrams = build_state_symbols(diagrams, self.symbol_changes.values())
        return diagrams

    def commit(self):
        # todo implement this!
        pass


def build_state_metadata(schemas, new_changes):
    """
    schemas is array of Schema 's representing current state
    new_changes are Change objects that need to be applied to current state
    """

    if schemas is None:
        schemas = []

    schema_changes = [x for x in new_changes if x.object_type == 'Schema']
    for schema_change in schema_changes:
        change_obj = change_to_object(schema_change)
        schema = [x for x in schemas if x.id == change_obj.id]
        schema = schema[0] if schema else None
        if schema_change.change_type == 0:
            schemas.append(change_obj)
        elif schema_change.change_type == 1:
            if schema is None:
                continue
            schema.collation = change_obj.collation
            schema.database_name = change_obj.database_name
            schema.comment = change_obj.comment
        else:  # remove shcema
            schemas.remove(schema)

    namespace_changes = [x for x in new_changes if x.object_type == 'Namespace']
    for namespace_change in namespace_changes:
        change_obj = change_to_object(namespace_change)

        schema_parent = [x for x in schemas if x.id == change_obj.schema_ref]
        schema_parent = schema_parent[0] if schema_parent else None
        namespace = [x for x in schema_parent.namespaces if x.id == change_obj.id][0]
        namespace = namespace[0] if namespace else None
        if namespace_change.change_type == 0:
            schema_parent.namespaces.append(change_obj)
        elif namespace_change.change_type == 1:
            if namespace is None:
                continue
            namespace = object
        else:  # remove namespace
            schema_parent.namespaces.remove(namespace)

    table_changes = [x for x in new_changes if x.object_type == 'Table']
    for table_change in table_changes:
        change_obj = change_to_object(table_change)
        schema_parent = [x for x in schemas if x.id == change_obj.schema_ref]
        schema_parent = schema_parent[0] if schema_parent else None
        table = [x for x in schema_parent.tables if x.id == change_obj.id]
        table = table[0] if table else None
        if table_change.change_type == 0:
            schema_parent.tables.append(change_obj)
        elif table_change.change_type == 1:
            if table is None:
                continue
            table.name = change_obj.name
            table.comment = change_obj.comment
            table.collation = change_obj.collation
            table.namespace_ref = change_obj.namespace_ref
        else:  # remove table
            schema_parent.remove(table)

    column_changes = [x for x in new_changes if x.object_type == 'Column']
    for column_change in column_changes:
        change_obj = change_to_object(column_change)

        table_parent = None
        for schema in schemas:
            for table in schema.tables:
                if change_obj.table_ref == table.id:
                    table_parent = table
        if table_parent is None:
            continue

        column = [x for x in table_parent.columns if x.id == change_obj.id]
        column = column[0] if column else None
        if column_change.change_type == 0:
            table_parent.columns.append(change_obj)
        elif column_change.change_type == 1:
            if column is None:
                continue
            column.name = change_obj.name
            column.comment = change_obj.comment
            column.comment = change_obj.comment
            column.column_type_ref = change_obj.column_type_ref
            column.length = change_obj.length
            column.precision = change_obj.precision
            column.default = change_obj.default
            column.collation = change_obj.collation
            column.ordinal = change_obj.ordinal
            column.is_primary_key = change_obj.is_primary_key
            column.is_nullable = change_obj.is_nullable
            column.is_unique = change_obj.is_unique
            column.is_auto_increment = change_obj.is_auto_increment
            column.dictionary = change_obj.dictionary
        else:  # remove column
            table_parent.remove(column)

    index_changes = [x for x in new_changes if x.object_type == 'Index']
    for index_change in index_changes:
        change_obj = change_to_object(index_change)

        table_parent = None
        for schema in schemas:
            for table in schema.tables:
                if change_obj.table_ref == table.id:
                    table_parent = table
        if table_parent is None:
            continue
        index = [x for x in table_parent.indexes if x.id == change_obj.id]
        index = index[0] if index else None
        if index_change.change_tpye == 0:
            table_parent.indexes.append(change_obj)
        elif index_change.change_tpye == 1:
            if index is None:
                continue
            index.name = change_obj.name
            index.storage_type = change_obj.storage_type
            index.comment = change_obj.comment
            index.columns = change_obj.columns
        else:  # remove index
            table_parent.indexes.remove(index)

    fk_changes = [x for x in new_changes if x.object_type == 'ForeignKey']
    for fk_change in fk_changes:
        change_obj = change_to_object(fk_change)

        table_parent = None
        for schema in schemas:
            for table in schema.tables:
                if change_obj.table_ref == table.id:
                    table_parent = table
        if table_parent is None:
            continue
        fk = [x for x in table_parent.foreign_keys if x.id == change_obj.id]
        fk = fk[0] if fk else None
        if fk_change.change_type == 0:
            table_parent.foreign_keys.append(change_obj)
        elif fk_change.change_type == 1:
            if fk is None:
                continue
            fk.name = change_obj.name
            fk.comment = change_obj.comment
            fk.on_update_referential_action = change_obj.on_update_referential_action
            fk.on_delete_referential_action = change_obj.on_delete_referential_action
            fk.source_columns = change_obj.source_columns
            fk.referenced_columns = change_obj.referenced_columns
        else:  # remove foreign key
            table_parent.foreign_keys.remove(fk)

    return schemas


def build_state_symbols(diagrams, new_changes):
    if diagrams is None:
        diagrams = []
    diagram_changes = [x for x in new_changes if x.object_type == 'Diagram']
    for diagram_change in diagram_changes:
        change_obj = change_to_object(diagram_change)
        diagram = [x for x in diagrams if x.id == change_obj.id]
        diagram = diagram[0] if diagram else None
        if diagram_change.change_type == 0:
            diagrams.append(change_obj)
        elif diagram_change.change_type == 1:
            if diagram is None:
                continue
            diagram.name = change_obj.name
            diagram.description = change_obj.description
        else:  # remove diagram
            diagrams.remove(diagram)
    layer_changes = [x for x in new_changes if x.object_type == 'Layer']
    for layer_change in layer_changes:
        change_obj = change_to_object(layer_change)

        diagram_parent = [x for x in diagrams if x.id == change_obj.diagram_ref]
        diagram_parent = diagram_parent[0] if diagram_parent else None
        layer = [x for x in diagram_parent.layers if x.id == change_obj.id]

        if layer_change.change_type == 0:
            diagram_parent.layers.append(change_obj)
        elif layer_change.change_type == 1:
            if layer is None:
                continue
            layer.name = change_obj.name
            layer.position_x = change_obj.position_x
            layer.position_y = change_obj.position_y
            layer.width = change_obj.width
            layer.height = change_obj.height
            layer.background_color = change_obj.background_color
        else:  # remove layer
            diagram_parent.layers.remove(layer)

    table_el_changes = [x for x in new_changes if x.object_type == 'TableElement']
    for table_el_change in table_el_changes:
        change_obj = change_to_object(table_el_change)

        diagram_parent = [x for x in diagrams if x.id == change_obj.diagram_ref]
        diagram_parent = diagram_parent[0] if diagram_parent else None
        table = [x for x in diagram_parent.table if x.id == change_obj.id]
        table = table[0] if table else None

        if table_el_change.change_type == 0:
            diagram_parent.tables.append(change_obj)
        elif table_el_change.change_type == 1:
            if table is None:
                continue
            table.position_x = change_obj.position_x
            table.position_y = change_obj.position_y
            table.width = change_obj.width
            table.height = change_obj.height
            table.color = change_obj.color
            table.is_collapsed = change_obj.is_collapsed
            table.layer_ref = change_obj.layer_ref
        else:  # remove table element
            diagram_parent.tables.remove(table)

    rel_el_changes = [x for x in new_changes if x.object_type == 'RelationshipElement']
    for rel_el_change in rel_el_changes:
        change_obj = change_to_object(rel_el_change)

        diagram_parent = [x for x in diagrams if x.id == change_obj.diagram_ref]
        diagram_parent = diagram_parent[0] if diagram_parent else None
        rel_el = [x for x in diagram_parent.relationship_elements if x.id == change_obj.id]
        rel_el = rel_el[0] if rel_el else None

        if rel_el_change.change_type == 0:
            diagram_parent.relationship_elements.append(rel_el)
        elif rel_el_change.change_type == 0:
            if rel_el is None:
                continue
            rel_el.start_position_x = change_obj.start_position_x
            rel_el.start_position_y = change_obj.start_position_y
            rel_el.end_position_x = change_obj.end_position_x
            rel_el.end_position_y = change_obj.end_position_y
            rel_el.draw_style = change_obj.draw_style
            rel_el.foreign_key_ref = change_obj.foreign_key_ref

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


