from uuid import uuid4
from django.db import models
from django.conf import settings


REFERENTIAL_ACTIONS = (
    (0, "NO ACTION"),
    (1, "RESTRICT "),
    (2, "CASCADE "),
    (3, "SET NULL "),
)


class Schema(object):
    def __init__(self):
        self.id = str(uuid4())
        self.database_name = ''
        self.comment = ''
        self.collation = ''

        self.namespaces = []
        self.tables = []


class Namespace(object):

    def __init__(self, id=None, name=None, comment=None, abbreviation=None):
        self.id = id
        self.name = name
        self.comment = comment
        self.abbreviation = abbreviation

        #project_ref = ''
        # TODO Implement: namespace.abbreviation unique within project


class Table(object):
    def __init__(self):
        self.id = str(uuid4())
        self.name = ''
        self.comment = ''
        self.collation = ''
        self.namespace_ref = ''
        self.columns = []
        self.indexes = []
        self.foreign_keys = []

    # TODO Implement: table.name unique within same namespace


class Column(object):
    def __init__(self):
        self.id = str(uuid4())
        self.name = ''
        self.comment = ''
        self.column_type_ref = ''
        self.length = ''
        self.precision = ''
        self.default = ''
        self.collation = ''
        self.ordinal = ''
        self.is_primary_key = False
        self.is_nullable = True
        self.is_unique = False
        self.is_auto_increment = False
        self.dictionary = False

        #table_ref = ''

    # TODO Implement: table.name unique within same namespace


class Index(object):
    def __init__(self):
        self.id = str(uuid4())
        self.name = ''
        self.storage_type = ''
        self.comment = ''
        self.self.columns = []


class ForeignKey(object):
    def __init__(self):
        self.id = str(uuid4())
        self.name = ''
        self.comment = ''
        self.on_update_referential_action = REFERENTIAL_ACTIONS
        self.on_delete_referential_action = REFERENTIAL_ACTIONS
        self.source_columns = []
        self.referenced_columns = []


class Diagram(object):
    def __init__(self):
        self.id = str(uuid4())
        self.name = ''
        self.comment = ''
        self.url = ''
        self.elements = []


class Layer(object):
    def __init__(self):
        self.id = str(uuid4())
        self.name = ''
        self.color_code = ''
        self.position_x = ''
        self.position_y = ''
        self.width = ''
        self.height = ''
        self.background_color = ''


class TableElement(object):
    def __init__(self):
        self.id = str(uuid4())
        self.position_x = ''
        self.position_y = ''
        self.width = ''
        self.height = ''
        self.color = ''
        self.is_collapsed = False
        self.table_ref = ''
        self.layer_ref = ''


class RelationshipElement(object):
    def __init__(self):
        self.id = str(uuid4())
        self.start_position_x = ''
        self.start_position_y = ''
        self.end_position_x = ''
        self.end_position_y = ''
        self.draw_style = ''
        self.foreign_key_ref = ''

