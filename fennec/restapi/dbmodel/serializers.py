from json.encoder import JSONEncoder
from rest_framework import serializers
from fennec.restapi.dbmodel.models import Index, ForeignKey, Schema, Layer, TableElement, RelationshipElement, Diagram
from models import Table, Namespace, Column
from json import JSONEncoder

#def serialize(obj):
#    if isinstance(obj, Table):
#        return TableSerializerFK(obj).data
#    elif isinstance(obj, Column):
#        return ColumnSerializerFK(obj).data
#    elif isinstance(obj,  Namespace):
#        return NamespaceSerializer(obj).data


class NamespaceSerializer(serializers.Serializer):
    id = serializers.CharField()
    abbreviation = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)

    schemaRef = serializers.CharField(source='schema_ref')

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.id = attrs.get('id', instance.id)
            instance.abbreviation = attrs.get('abbreviation', instance.abbreviation)
            instance.name = attrs.get('name', instance.name)
            instance.comment = attrs.get('comment', instance.comment)
            return instance
        print "attrs:" + str(attrs)
        return Namespace(**attrs)


class ColumnSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    column_type_ref = serializers.CharField()
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
    columns = ColumnSerializer(required=False)

    tableRef = serializers.CharField(source='tableRef')

    def restore_object(self, attrs, instance=None):
        return Index(**attrs)


class ForeignKeySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    onUpdate = serializers.IntegerField(source='on_update_referential_action')
    onDelete = serializers.IntegerField(source='on_delete_referential_action')
    sourceColumns = ColumnSerializer(required=False, source='source_columns')
    referencedColumns = ColumnSerializer(required=False, source='referenced_columns')

    tableRef = serializers.CharField(source='tableRef')

    def restore_object(self, attrs, instance=None):
        return ForeignKey(**attrs)


class TableSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField(required=False)
    collation = serializers.CharField(required=False)
    namespaceRef = serializers.CharField(source='namespace_ref', required=False)
    columns = ColumnSerializer(required=False)
    indexes = IndexSerializer(required=False)
    foreignKeys = ForeignKeySerializer(required=False, source='foreign_keys')

    schemaRef = serializers.CharField(source='schema_ref')

    def restore_object(self, attrs, instance=None):
        return Table(**attrs)


class SchemaSerializer(serializers.Serializer):
    id = serializers.CharField()
    database_name = serializers.CharField()
    comment = serializers.CharField(required=False)
    collation = serializers.CharField()

    namespaces = NamespaceSerializer(required=False)
    tables = TableSerializer(required=False)

    def restore_object(self, attrs, instance=None):
        return Schema(**attrs)


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
    collapsed = serializers.BooleanField(source='is_collapsed')
    tableRef = serializers.CharField(source='table_ref')
    layerRef = serializers.CharField(source='layer_ref')

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
    #url = serializers.FloatField(source='position_y')
    layers = LayerSerializer(required=False)
    tableElements = TableElementSerializer(required=False, source='table_elements')
    relationshipElements = RelationshipElementSerializer(required=False, source='relationship_elements')

    def restore_object(self, attrs, instance=None):
        return Diagram(**attrs)

