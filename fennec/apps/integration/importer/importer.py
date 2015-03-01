from fennec.apps.diagram.serializers import TableSerializer, ColumnSerializer, IndexSerializer, SchemaSerializer
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
                # for index in table.indexes:
                #     self.__save_index_change__(index)

    def __save_schema_change__(self, schema):
        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Schema'
        change.object_code = schema.id

        serializer = SchemaSerializer(schema, remove_fields=['namespaces', 'tables'])
        change.content = serializer.data
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_table_change__(self, table):
        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Table'
        change.object_code = table.id

        serializer = TableSerializer(table, remove_fields=['columns', 'indexes', 'foreignKeys'])
        change.content = serializer.data
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_column_change__(self, column):
        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Column'
        change.object_code = column.id
        serializer = ColumnSerializer(column)
        change.content = serializer.data
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_index_change__(self, index):
        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Index'
        change.object_code = index.id
        serializer = IndexSerializer()
        change.content = serializer.data
        change.save()
        self.__save_branch_revision_change__(change)

    def __save_branch_revision_change__(self, change):
        br_change = BranchRevisionChange()
        br_change.branch_revision_ref = self.branch_rev
        br_change.change_ref = change
        # br_change.id = ordinal
        br_change.save()