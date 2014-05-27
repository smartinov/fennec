from rest_framework import serializers

from models import TableSymbol


class TableSymbolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TableSymbol
        fields = ('id', 'position_x', 'position_y', 'width', 'height', 'color', 'is_collapsed')

