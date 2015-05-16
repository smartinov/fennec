from rest_framework.renderers import JSONRenderer

from fennec.apps.metamodel.serializers import ColumnSerializer, BasicSchemaSerializer, BasicTableSerializer, BasicIndexSerializer, \
    ForeignKeyBasicSerializer
from fennec.apps.repository.models import BranchRevisionChange
from fennec.apps.metamodel.models import Change


__author__ = 'Darko'


class FennecImporter():
    def __init__(self, model=None, user=None, branch_rev=None):
        self.model = model if model else []
        self.user = user
        self.branch_rev = branch_rev

    def import_model(self):
        for schema in self.model:
            self.__save_schema_change(schema)
            for table in schema.tables:
                self.__save_table_change(table)
                for column in table.columns:
                    self.__save_column_change(column)
                for index in table.indexes:
                    self.__save_index_change(index)
                for fk in table.foreign_keys:
                    self.__save_foreign_key_change(fk)

    def __save_schema_change(self, schema):
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
        self.__save_branch_revision_change(change)

    def __save_table_change(self, table):
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
        self.__save_branch_revision_change(change)

    def __save_column_change(self, column):
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
        self.__save_branch_revision_change(change)

    def __save_index_change(self, index):
        serializer = BasicIndexSerializer(index)
        json = JSONRenderer().render(serializer.data)

        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'Index'
        change.object_code = index.id
        change.content = json
        change.save()
        self.__save_branch_revision_change(change)

    def __save_foreign_key_change(self, foreign_key):
        serializer = ForeignKeyBasicSerializer(foreign_key)
        json = JSONRenderer().render(serializer.data)

        change = Change()
        change.change_type = 0
        change.is_ui_change = False
        change.made_by = self.user
        change.object_type = 'ForeignKey'
        change.object_code = foreign_key.id
        change.content = json
        change.save()
        self.__save_branch_revision_change(change)


    def __save_branch_revision_change(self, change):
        br_change = BranchRevisionChange()
        br_change.branch_revision_ref = self.branch_rev
        br_change.change_ref = change
        # br_change.id = ordinal
        br_change.save()