REFERENTIAL_ACTIONS = (
    (0, "NO ACTION"),
    (1, "RESTRICT "),
    (2, "CASCADE "),
    (3, "SET NULL "),
)


class Schema(object):
    def __init__(self, **kwargs):
        """
        :type id: int
        :return:
        """
        self.id = kwargs.get('id')
        self.database_name = kwargs.get('database_name')
        self.comment = kwargs.get('comment')
        self.collation = kwargs.get('collation')
        self.namespaces = kwargs.get('namespaces', [])
        self.tables = kwargs.get('tables', [])


class Namespace(object):
    def __init__(self, id=None, name=None, comment=None, abbreviation=None, schema_ref=None):
        self.id = id
        self.name = name
        self.comment = comment
        self.abbreviation = abbreviation

        self.schema_ref = schema_ref
        # TODO Implement: namespace.abbreviation unique within project


class Table(object):
    def __init__(self, id=None, name=None, comment=None, collation=None, namespace_ref=None, columns=None, indexes=None,
                 foreign_keys=None, schema_ref=None):
        if columns is None:
            columns = []
        self.id = id
        self.name = name
        self.comment = comment
        self.collation = collation
        self.namespace_ref = namespace_ref
        self.columns = columns if columns else []
        self.indexes = indexes if indexes else []
        self.foreign_keys = foreign_keys if foreign_keys else []

        self.schema_ref = schema_ref
        # TODO Implement: table.name unique within same namespace


class Column(object):
    def __init__(self, id=None, name=None, comment=None, column_type=None, length=None, precision=None,
                 default=None, collation=None, ordinal=None, is_primary_key=False, is_nullable=True, is_unique=False,
                 is_auto_increment=False, dictionary=False, table_ref=None):
        self.id = id
        self.name = name
        self.comment = comment
        self.column_type = column_type
        self.length = length
        self.precision = precision
        self.default = default
        self.collation = collation
        self.ordinal = ordinal
        self.is_primary_key = is_primary_key
        self.is_nullable = is_nullable
        self.is_unique = is_unique
        self.is_auto_increment = is_auto_increment
        self.dictionary = dictionary

        self.table_ref = table_ref

        # TODO Implement: table.name unique within same namespace


class Index(object):
    def __init__(self, id=None, name=None, storage_type=None, comment=None, columns=[], table_ref=None):
        self.id = id
        self.name = name
        self.storage_type = storage_type
        self.comment = comment
        self.columns = columns if columns else []

        self.table_ref = table_ref


class ForeignKey(object):
    def __init__(self, id=None, name=None, comment=None, on_update_referential_action=REFERENTIAL_ACTIONS[0],
                 on_delete_referential_action=REFERENTIAL_ACTIONS[0], source_columns=[], referenced_columns=[],
                 table_ref=None):
        self.id = id
        self.name = name
        self.comment = comment
        self.on_update_referential_action = on_update_referential_action
        self.on_delete_referential_action = on_delete_referential_action
        self.source_columns = source_columns if source_columns else []
        self.referenced_columns = referenced_columns if referenced_columns else []

        self.table_ref = table_ref


class Diagram(object):
    def __init__(self, id=None, name=None, description=None, layers=[], table_elements=[],
                 relationship_elements=[]):
        self.id = id
        self.name = name
        self.description = description
        self.layers = layers if layers else []
        self.table_elements = table_elements if table_elements else []
        self.relationship_elements = relationship_elements if relationship_elements else []


class Layer(object):
    def __init__(self, id=None, name=None, position_x=None, position_y=None, width=None, height=None,
                 background_color=None, diagram_ref=None):
        self.id = id
        self.name = name
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.background_color = background_color

        self.diagram_ref = diagram_ref


class TableElement(object):
    def __init__(self, id=None, position_x=None, position_y=None, width=None, height=None, color=None,
                 is_collapsed=False, table_ref=None, layer_ref=None, diagram_ref=None):
        self.id = id
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.color = color
        self.is_collapsed = is_collapsed
        self.table_ref = table_ref
        self.layer_ref = layer_ref

        self.diagram_ref = diagram_ref


class RelationshipElement(object):
    def __init__(self, id=None, start_position_x=None, start_position_y=None, end_position_x=None, end_position_y=None,
                 draw_style=None, foreign_key_ref=None, diagram_ref=None):
        self.id = id
        self.start_position_x = start_position_x
        self.start_position_y = start_position_y
        self.end_position_x = end_position_x
        self.end_position_y = end_position_y
        self.draw_style = draw_style
        self.foreign_key_ref = foreign_key_ref

        self.diagram_ref = diagram_ref


