from uuid import uuid4
from rest_framework.renderers import JSONRenderer
from fennec.apps.diagram.serializers import TableSerializer, ColumnSerializer, IndexSerializer, SchemaSerializer, \
    BasicSchemaSerializer, BasicTableSerializer, BasicIndexSerializer
from fennec.apps.diagram.utils import Schema
from fennec.apps.versioncontroll.models import Change, CHANGE_TYPE, BranchRevisionChange

__author__ = 'Darko'


class FennecImporter():

    def __init__(self, model =None, user=None, branch_rev=None):
        self.model = model if model else []
        self.user = user
        self.branch_rev = branch_rev

    def import_model(self):
        for schema in self.model:
            self.__save_schema_change__(schema)
            for table in schema.tables:
                self.__save_table_change__(table)
                for column in table.columns:
                    self.__save_column_change__(column)
                for index in table.indexes:
                    self.__save_index_change__(index)

    def __save_schema_change__(self, schema):
        serializer = BasicSchemaSerializer(schema)
        json = JSONRenderer().render(serializer.data)

        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Schema'
        change.object_code = schema.id
        change.content = json
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_table_change__(self, table):
        serializer = BasicTableSerializer(table)
        json = JSONRenderer().render(serializer.data)

        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Table'
        change.object_code = table.id

        change.content = json
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_column_change__(self, column):
        serializer = ColumnSerializer(column)
        json = JSONRenderer().render(serializer.data)

        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Column'
        change.object_code = column.id
        change.content = json
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_index_change__(self, index):
        serializer = BasicIndexSerializer(index)
        if not serializer.is_valid():
            print serializer.errors
        json = JSONRenderer().render(serializer.data)

        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Index'
        change.object_code = index.id
        change.content = json
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_branch_revision_change__(self, change):
        br_change = BranchRevisionChange()
        br_change.branch_revision_ref = self.branch_rev
        br_change.change_ref = change
        # br_change.id = ordinal
        br_change.save()