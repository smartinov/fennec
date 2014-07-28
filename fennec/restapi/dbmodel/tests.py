from django.test import TestCase
from django.core import serializers

# Create your tests here.
from rest_framework.serializers import ModelSerializer
from fennec.restapi.dbmodel.models import Table, Sandbox, Namespace
from fennec.restapi.dbmodel.serializers import TableSerializerFK


class ExampleTestCase(TestCase):
    #def setUp(self):

    def test_table_tojson(self):
        s = Namespace()
        s.id = 1

        t = Table()
        t.id = 1
        t.name = "test"
        t.prepare_database_save = "t"
        t.namespace_ref = s


        #serializer = TableSerializerFK(t)
        #print serializer.data
        #ses = TableSerializerFK(data=serializer.data)

        #print ses.is_valicd()
        #print "{0} {1}".format(t1.id, t1.description)
        #json = serializers.serialize('json', [t, ])
        #
        #print json
        #
        #t1 = Table(serializers.deserialize('json', json))
        #print 'obj'
        #print t1.id
        #print t1.name
        #print t1.sandbox_ref