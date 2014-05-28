from rest_framework import serializers

from models import Diagram, Layer, TableSymbol, ColumnSymbol


class DiagramSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Diagram
        fields = ('id', 'name', 'description', 'project_ref')


class LayerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Layer
        fields = ('id', 'name', 'color_code', 'diagram_ref')


class TableSymbolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TableSymbol
        fields = ('id', 'position_x', 'position_y', 'width', 'height', 'color', 'is_collapsed')


class ColumnSymbolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ColumnSymbol
        fields = ('id', 'is_visible', 'table_symbol_ref', 'column_ref')
