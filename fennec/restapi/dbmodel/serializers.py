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
    comment = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.id = attrs.get('id', instance.id)
            instance.abbreviation = attrs.get('abbreviation', instance.abbreviation)
            instance.name = attrs.get('name', instance.name)
            instance.comment = attrs.get('comment', instance.comment)
            return instance
        return Namespace(**attrs)


class ColumnSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField()
    column_type_ref = serializers.CharField()
    length = serializers.IntegerField()
    precision = serializers.FloatField()
    default = serializers.CharField()
    collation = serializers.CharField()
    ordinal = serializers.IntegerField()
    is_primary_key = serializers.BooleanField()
    is_nullable = serializers.BooleanField()
    is_unique = serializers.BooleanField()
    is_auto_increment = serializers.BooleanField()
    dictionary = serializers.BooleanField()

    def restore_object(self, attrs, instance=None):
        return Column(**attrs)

class IndexSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField()
    storage_type = serializers.CharField()
    columns = ColumnSerializer(required=False)

    def restore_object(self, attrs, instance=None):
        return Index(**attrs)


class ForeignKeySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.CharField()
    on_update_referential_action = serializers.IntegerField()
    on_delete_referential_action = serializers.IntegerField()
    source_columns = ColumnSerializer(required=False)
    referenced_columns = ColumnSerializer(required=False)

    def restore_object(self, attrs, instance=None):
        return ForeignKey(**attrs)

class TableSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment= serializers.CharField()
    collation = serializers.CharField()
    namespace_ref = serializers.CharField()
    columns = ColumnSerializer(required=False)
    indexes = IndexSerializer(required=False)
    foreign_keys = ForeignKeySerializer(required=False)

    def restore_object(self, attrs, instance=None):
        return Table(**attrs)

class SchemaSerializer(serializers.Serializer):
    id = serializers.CharField()
    database_name = serializers.CharField()
    comment = serializers.CharField()
    collation = serializers.CharField()

    namespaces = NamespaceSerializer(required=False)
    tables = TableSerializer(required=False)

    def restore_object(self, attrs, instance=None):
        return Schema(**attrs)

class LayerSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    backgroundColor = serializers.CharField(source='background_color')
    positionX = serializers.FloatField(source='position_x')
    positionY = serializers.FloatField(source='position_y')
    width = serializers.FloatField()
    height = serializers.FloatField()

    def restore_object(self, attrs, instance=None):
        return Layer(**attrs)

class TableElementSerializer(serializers.Serializer):
    id = serializers.CharField()
    color = serializers.CharField()
    positionX = serializers.FloatField(source='position_x')
    positionY = serializers.FloatField(source='position_y')
    width = serializers.FloatField()
    height = serializers.FloatField()
    is_collapsed = serializers.BooleanField()
    tableRef = serializers.CharField(source='table_ref')
    layerRef = serializers.CharField(source='layer_ref')

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
    
    def restore_object(self, attrs, instance=None):
        return RelationshipElement(**attrs)

class DiagramSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    comment = serializers.FloatField(source='position_x')
    #url = serializers.FloatField(source='position_y')

    def restore_object(self, attrs, instance=None):
        return Diagram(**attrs)

