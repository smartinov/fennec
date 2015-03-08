import json
from unittest import TestCase

from fennec.apps.metamodel.models import Change
from fennec.apps.metamodel.services import convert_change_to_object
from fennec.apps.metamodel.utils import Schema, Namespace


class TestChange_to_object(TestCase):
    def test_change_to_object_schema(self):
        data = Schema()
        data.id = 20
        data.namespaces = ['one', 'two']
        data.tables = ['table_one', 'table_two']
        data.comment = 'comment'
        data.collation = 'ucs2'
        data.database_name
        change = Change()

        change.object_type = data.__class__.__name__
        change.content = json.dumps(data.__dict__)

        object = convert_change_to_object(change)
        self.assertEqual(object.__class__, data.__class__)
        self.assertDictEqual(object.__dict__, data.__dict__)

    def test_change_to_object_namespace(self):
        data = Namespace()
        data.id = 20
        data.abbreviation = 'NSP'
        data.name = 'Namespace'
        data.schema_ref = 20
        data.namespaces = ['one', 'two']
        data.tables = ['table_one', 'table_two']
        data.comment = 'comment'
        change = Change()

        change.object_type = data.__class__.__name__
        change.content = json.dumps(data.__dict__)

        object = convert_change_to_object(change)
        self.assertEqual(object.__class__, data.__class__)
        self.assertDictEqual(object.__dict__, data.__dict__)

    def test_change_to_object_namespace(self):
        self.fail()

    def test_change_to_object_table(self):
        self.fail()

    def test_change_to_object_column(self):
        self.fail()

    def test_change_to_object_index(self):
        self.fail()

    def test_change_to_object_foreign_key(self):
        self.fail()

    def test_change_to_object_layer(self):
        self.fail()

    def test_change_to_object_table_element(self):
        self.fail()

    def test_change_to_object_relationship_element(self):
        self.fail()