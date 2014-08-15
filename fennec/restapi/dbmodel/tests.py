from StringIO import StringIO
from uuid import uuid4
from django.core import serializers
from django.test import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from fennec.restapi.dbmodel.models import Schema
from fennec.restapi.dbmodel.serializers import SchemaSerializer
from serializers import NamespaceSerializer
from models import Namespace


class ModelTest(TestCase):

    def test_namespace_serializer(self):


        ns = Namespace()
        ns.id = str(uuid4())
        ns.comment = "test"
        ns.abbreviation = "ASD"
        ns.name = "TEST"

        serializer = NamespaceSerializer(ns)
        json = JSONRenderer().render(serializer.data)
        print json
        self.assertEqual(ns.name, serializer.data['name'])
        self.assertEqual(ns.abbreviation, serializer.data['abbreviation'])
        self.assertEqual(ns.id, serializer.data['id'])



        sh = Schema()
        sh.id = str(uuid4())
        sh.collation = "test collation"
        sh.comment = "whatever"
        sh.database_name = "testDB"
        sh.namespaces.append(ns)

        sh_serializer = SchemaSerializer(sh)
        #print JSONRenderer().render(sh_serializer.data)

        stream = StringIO(json)
        s = NamespaceSerializer(data=JSONParser().parse(stream))
        print s.object
        print s.is_valid()
