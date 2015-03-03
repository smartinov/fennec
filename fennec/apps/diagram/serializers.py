from rest_framework import serializers

from fennec.apps.diagram.utils import Index, ForeignKey, Schema, Layer, TableElement, RelationshipElement, Diagram
from fennec.apps.diagram.utils import Table, Namespace, Column


class NamespaceSerializer(serializers.Serializer):
    id = serializers.CharField()
    abbreviation = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)

    schemaRef = serializers.CharField(source='schema_ref')

    def restore_object(self, attrs, instance=None):
        return Namespace(**attrs)


class ColumnSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    column_type = serializers.CharField()
    length = serializers.IntegerField()
    precision = serializers.FloatField(required=False)
    default = serializers.CharField(required=False)
    collation = serializers.CharField(required=False)
    ordinal = serializers.IntegerField()
    primary = serializers.BooleanField(source='is_primary_key')
    nullable = serializers.BooleanField(source='is_nullable')
    unique = serializers.BooleanField(source='is_unique')
    autoIncrement = serializers.BooleanField(source='is_auto_increment')
    dictionary = serializers.BooleanField()

    tableRef = serializers.CharField(source='table_ref')

    def restore_object(self, attrs, instance=None):
        return Column(**attrs)


class IndexSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    storageType = serializers.CharField(source='storage_type')
    columns = ColumnSerializer(required=False, many=True)

    tableRef = serializers.CharField(source='tableRef')

    def restore_object(self, attrs, instance=None):
        index = Index(**attrs)
        index.columns = []
        return index


class BasicIndexSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    storageType = serializers.CharField(source='storage_type')
    tableRef = serializers.CharField(source='tableRef')


class ForeignKeySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    onUpdate = serializers.IntegerField(source='on_update_referential_action')
    onDelete = serializers.IntegerField(source='on_delete_referential_action')
    sourceColumns = ColumnSerializer(required=False, source='source_columns', many=True)
    referencedColumns = ColumnSerializer(required=False, source='referenced_columns', many=True)

    tableRef = serializers.CharField(source='tableRef')

    def restore_object(self, attrs, instance=None):
        foreign_key = ForeignKey(**attrs)
        foreign_key.source_columns = []
        foreign_key.referenced_columns = []
        return foreign_key


class TableSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    collation = serializers.CharField(required=False)
    namespaceRef = serializers.CharField(source='namespace_ref', required=False)
    columns = ColumnSerializer(required=False, many=True)
    indexes = IndexSerializer(required=False, many=True)
    foreignKeys = ForeignKeySerializer(required=False, source='foreign_keys', many=True)

    schemaRef = serializers.CharField(source='schema_ref')

    def restore_object(self, attrs, instance=None):
        table = Table(**attrs)
        table.columns = []
        table.indexes = []
        table.foreign_keys = []
        return table


class BasicTableSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    collation = serializers.CharField(required=False)
    namespaceRef = serializers.CharField(source='namespace_ref', required=False)
    schemaRef = serializers.CharField(source='schema_ref')


class SchemaSerializer(serializers.Serializer):
    id = serializers.CharField()
    databaseName = serializers.CharField(source='database_name')
    comment = serializers.CharField(required=False)
    collation = serializers.CharField()

    namespaces = NamespaceSerializer(required=False, many=True)
    tables = TableSerializer(required=False, many=True)

    def restore_object(self, attrs, instance=None):
        schema = Schema(**attrs)
        schema.namespaces = []
        schema.tables = []
        return schema


class BasicSchemaSerializer(serializers.Serializer):
    id = serializers.CharField()
    databaseName = serializers.CharField(source='database_name')
    comment = serializers.CharField(required=False)
    collation = serializers.CharField()


class LayerSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(required=False)
    backgroundColor = serializers.CharField(source='background_color')
    positionX = serializers.FloatField(source='position_x')
    positionY = serializers.FloatField(source='position_y')
    width = serializers.FloatField()
    height = serializers.FloatField()

    diagramRef = serializers.CharField(source='diagram_ref')

    def restore_object(self, attrs, instance=None):
        return Layer(**attrs)


class TableElementSerializer(serializers.Serializer):
    id = serializers.CharField()
    color = serializers.CharField()
    positionX = serializers.FloatField(source='position_x')
    positionY = serializers.FloatField(source='position_y')
    width = serializers.FloatField()
    height = serializers.FloatField()
    collapsed = serializers.BooleanField(source='is_collapsed', required=False)
    tableRef = serializers.CharField(source='table_ref')
    layerRef = serializers.CharField(source='layer_ref', required=False)

    diagramRef = serializers.CharField(source='diagram_ref')

    def restore_object(self, attrs, instance=None):
        return TableElement(**attrs)


class RelationshipElementSerializer(serializers.Serializer):
    id = serializers.CharField()
    startPositionX = serializers.FloatField(source='start_position_x')
    startPositionY = serializers.FloatField(source='start_position_y')
    endPositionX = serializers.FloatField(source='end_position_x')
    endPositionX = serializers.FloatField(source='end_position_y')
    drawStyle = serializers.IntegerField(source='draw_style')
    foreignKeyRef = serializers.CharField(source='foreign_key_ref')

    diagramRef = serializers.CharField(source='diagram_ref')

    def restore_object(self, attrs, instance=None):
        return RelationshipElement(**attrs)


class DiagramSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    layers = LayerSerializer(required=False, many=True)
    tableElements = TableElementSerializer(required=False, source='table_elements', many=True)
    relationshipElements = RelationshipElementSerializer(required=False, source='relationship_elements', many=True)

    def restore_object(self, attrs, instance=None):
        diagram = Diagram(**attrs)
        diagram.layers = []
        diagram.table_elements = []
        diagram.relationship_elements = []
        return diagram


class BranchBasicInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    revision = serializers.IntegerField()


class ProjectInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    url = serializers.URLField()
    branch = BranchBasicInfoSerializer()


class DiagramBasicInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    url = serializers.URLField()


class SandboxBasicInfoSerializer(serializers.Serializer):
    project = ProjectInfoSerializer(source='project_info')
    diagrams = DiagramBasicInfoSerializer(many=True)
    schemas = SchemaSerializer(many=True)


