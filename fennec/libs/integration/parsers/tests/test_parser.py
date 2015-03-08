import os
from unittest.case import TestCase

from fennec.libs.integration.parsers.mysql.workbench.parser import WorkbenchParser


__author__ = 'Darko'


class WorkbenchParserTest(TestCase):
    def test_parsing_from_file(self):
        path = self.get_path('samplemodel.mwb')
        parser = WorkbenchParser()
        schemas = parser.parse_file(path)
        self.assertEquals(1, len(schemas))
        schema = schemas[0]
        self.assertEquals(3, len(schema.tables))
        students_table = schema.tables[0]
        self.assertEquals("Students", students_table.name)
        self.assertEquals("Students table, simple as that.", students_table.comment)
        self.assertEquals(2, len(students_table.indexes))
        student_id_column = students_table.columns[0]
        self.assertEquals("ID", student_id_column.name)
        self.assertEquals("INT", student_id_column.column_type)
        self.assertEquals(False,  student_id_column.is_nullable)

    @staticmethod
    def get_path(path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', path.lstrip('/'))