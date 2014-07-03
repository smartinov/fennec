from rest_framework import serializers
from models import Table, Namespace, Column


def serialize(obj):
    if isinstance(obj, Table):
        return TableSerializerFK(obj).data
    elif isinstance(obj, Column):
        return ColumnSerializerFK(obj).data
    elif isinstance(obj,  Namespace):
        return NamespaceSerializerFK(obj).data


class NamespaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Namespace
        fields = ('id', 'abbreviation', 'name', 'description', 'project_ref', 'parent_ref')


class NamespaceSerializerFK(serializers.ModelSerializer):
    class Meta:
        model = Namespace
        fields = ('id', 'abbreviation', 'name', 'description', 'project_ref', 'parent_ref')


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'name', 'description', 'collation', 'namespace_ref')


class TableSerializerFK(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'name', 'description', 'collation', 'namespace_ref')


class ColumnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'name', 'data_type', 'length', 'default_value', 'ordinal', 'description', 'is_primary_key', 'is_nullable', 'is_unique', 'is_auto_increment', 'table_ref')


class ColumnSerializerFK(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'name', 'data_type', 'length', 'default_value', 'ordinal', 'description', 'is_primary_key', 'is_nullable', 'is_unique', 'is_auto_increment', 'table_ref')


