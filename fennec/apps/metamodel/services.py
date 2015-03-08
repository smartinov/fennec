import json

from fennec.apps.metamodel.serializers import SchemaSerializer, NamespaceSerializer, TableSerializer, ColumnSerializer, \
    IndexSerializer, ForeignKeySerializer, DiagramSerializer, LayerSerializer, TableElementSerializer, \
    RelationshipElementSerializer


__author__ = 'stefan.martinov@gmail.com'

serializer_mappings = {
    'Schema': SchemaSerializer,
    'Namespace': NamespaceSerializer,
    'Table': TableSerializer,
    'Column': ColumnSerializer,
    'Index': IndexSerializer,
    'ForeignKey': ForeignKeySerializer,
    'Diagram': DiagramSerializer,
    'Layer': LayerSerializer,
    'TableElement': TableElementSerializer,
    'RelationshipElement': RelationshipElementSerializer
}

#TODO: Add comments how to use this function
def convert_change_to_object(change):
    """
    Converts the passed change to an object, to be later parsed
    :type change: fennec.apps.metamodel.models.Change
    :param change: Required Change
    :return:
    :rtype:
    """
    data = json.loads(change.content)

    serializer_type = serializer_mappings[change.object_type]
    serializer = serializer_type(data=data)
    if not serializer.is_valid():
        print serializer.errors

    return serializer.object