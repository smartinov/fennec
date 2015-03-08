from StringIO import StringIO
from rest_framework.parsers import JSONParser
from fennec.apps.metamodel.serializers import SchemaSerializer, NamespaceSerializer, TableSerializer, ColumnSerializer, \
    IndexSerializer, ForeignKeySerializer, DiagramSerializer, LayerSerializer, TableElementSerializer, \
    RelationshipElementSerializer

__author__ = 'stefan.martinov@gmail.com'


def convert_change_to_object(change):
    """
    Converts the passed change to an object, to be later parsed
    :type change: fennec.apps.metamodel.models.Change
    :param change: Required Change
    :return:
    """
    stream = StringIO(change.content)
    # print "Change content:"  + str(change.content)
    data = {}
    try:
        data = JSONParser().parse(stream)
    except Exception as e:
        pass

    serializer = switch_type(change.object_type)(data=data)
    if not serializer.is_valid():
        print serializer.errors

    return serializer.object


def switch_type(object_type):
    return {
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
    }.get(object_type, None)