import json
from unittest import TestCase

from fennec.apps.metamodel.models import Change
from fennec.apps.metamodel.services import convert_change_to_object


class TestChange_to_object(TestCase):
    def validate_serialization(self, object):
        change = Change()
        change.object_type = object.__class__.__name__
        change.content = json.dumps(object.__dict__)

        object = convert_change_to_object(change)
        self.assertEqual(object.__class__, object.__class__)
        self.assertDictEqual(object.__dict__, object.__dict__)
