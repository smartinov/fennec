REFERENTIAL_ACTIONS = (
    (0, "NO ACTION"),
    (1, "RESTRICT "),
    (2, "CASCADE "),
    (3, "SET NULL "),
)


class Schema(object):
    def __init__(self, **kwargs):
        """
        :type id: uuid4
        :return:
        """
        self.id = kwargs.get('id')
        self.database_name = kwargs.get('database_name')
        self.comment = kwargs.get('comment')
        self.collation = kwargs.get('collation')
        self.namespaces = kwargs.get('namespaces', [])
        self.tables = kwargs.get('tables', [])


class Namespace(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.comment = kwargs.get('comment')
        self.abbreviation = kwargs.get('abbreviation')

        self.schema_ref = kwargs.get('schema_ref')
        # TODO Implement: namespace.abbreviation unique within project


class Table(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.comment = kwargs.get('comment')
        self.collation = kwargs.get('collation')
        self.namespace_ref = kwargs.get('namespace_ref')
        self.columns = kwargs.get('columns') if kwargs.get('columns') else []
        self.indexes = kwargs.get('indexes') if kwargs.get('indexes') else []
        self.foreign_keys = kwargs.get('foreign_keys') if kwargs.get('foreign_keys') else []

        self.schema_ref = kwargs.get('schema_ref')
        # TODO Implement: table.name unique within same namespace


class Column(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.comment = kwargs.get('comment')
        self.column_type = kwargs.get('column_type')
        self.length = kwargs.get('length')
        self.precision = kwargs.get('precision')
        self.default = kwargs.get('default')
        self.collation = kwargs.get('collation')
        self.ordinal = kwargs.get('ordinal')
        self.is_primary_key = kwargs.get('is_primary_key')
        self.is_nullable = kwargs.get('is_nullable')
        self.is_unique = kwargs.get('is_unique')
        self.is_auto_increment = kwargs.get('is_auto_increment')
        self.dictionary = kwargs.get('dictionary')

        self.table_ref = kwargs.get('table_ref')

        # TODO Implement: table.name unique within same namespace


class Index(object):
    def __init__(self, **kwargs):
        """
        columns is array of index columns id's
        """
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.storage_type = kwargs.get('storage_type')
        self.comment = kwargs.get('comment')
        self.columns = kwargs.get('columns') if kwargs.get('columns') else []
        self.table_ref = kwargs.get('table_ref')


class ForeignKey(object):
    def __init__(self, **kwargs):
        """
        source_column is source columns id,
        referenced_columns is referenced columns id
        """
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.comment = kwargs.get('comment')
        self.on_update_referential_action = kwargs.get('on_update_referential_action')
        self.on_delete_referential_action = kwargs.get('on_delete_referential_action')
        self.source_column = kwargs.get('source_column')
        self.referenced_column = kwargs.get('referenced_column')

        self.table_ref = kwargs.get('table_ref')
        self.referenced_table_ref = kwargs.get('referenced_table_ref')


class Diagram(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.layers = kwargs.get('layers') if kwargs.get('layers') else []
        self.table_elements = kwargs.get('table_elements') if kwargs.get('table_elements') else []
        self.relationship_elements = kwargs.get('relationship_elements') if kwargs.get('relationship_elements') else []


class Layer(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.position_x = kwargs.get('position_x')
        self.position_y = kwargs.get('position_y')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.background_color = kwargs.get('background_color')

        self.diagram_ref = kwargs.get('diagram_ref')


class TableElement(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.position_x = kwargs.get('position_x')
        self.position_y = kwargs.get('position_y')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.color = kwargs.get('color')
        self.is_collapsed = kwargs.get('is_collapsed')
        self.table_ref = kwargs.get('table_ref')
        self.layer_ref = kwargs.get('layer_ref')

        self.diagram_ref = kwargs.get('diagram_ref')


class RelationshipElement(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.start_position_x = kwargs.get('start_position_x')
        self.start_position_y = kwargs.get('start_position_y')
        self.end_position_x = kwargs.get('end_position_x')
        self.end_position_y = kwargs.get('end_position_y')
        self.draw_style = kwargs.get('draw_style')
        self.cardinality = kwargs.get('cardinality')
        self.foreign_key_ref = kwargs.get('foreign_key_ref')

        self.diagram_ref = kwargs.get('diagram_ref')


