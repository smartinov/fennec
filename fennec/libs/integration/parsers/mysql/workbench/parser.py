import sys

__author__ = 'stefan.martinov@danulabs.com'

from xml.etree import ElementTree
from zipfile import ZipFile
import os

from fennec.apps.metamodel.utils import Table, Column, Index, Schema, ForeignKey, REFERENTIAL_ACTIONS


class WorkbenchParser():
    def __init__(self):
        pass

    def parse_file(self, path):
        """
        Parses the model from a file
        :type path: str
        :rtype: list of Table
        """
        if os.path.exists(path):
            model_data = self.__unpack_model(path)
            return self.__parse_model(model_data)
        else:
            raise IOError("File not found on path '%s'" % os.path.abspath(path))


    def __parse_model(self, model_data):
        """
        Parses the model to the workbench columns
        :type model_data: str
        :return:
        """
        self.model = ElementTree.ElementTree(ElementTree.fromstring(model_data))
        self.user_types = self.__parse_model_user_types()

        schemas = []
        for schema_element in self.model.findall('.//value[@type="object"][@struct-name="db.mysql.Schema"]'):
            schema = self.__get_schema(schema_element)
            schemas.append(schema)

            schema.tables = []
            for table_element in schema_element.findall('.//value[@type="object"][@struct-name="db.mysql.Table"]'):
                table = self.__get_table(table_element)
                table.schema_ref = schema.id
                schema.tables.append(table)
                col_ordinal = 0

                query = '.value[@key="columns"]/value[@struct-name="db.mysql.Column"]'
                for column_element in table_element.findall(query):
                    column = self.__get_column(column_element, col_ordinal)
                    column.table_ref = table.id
                    table.columns.append(column)
                    col_ordinal += 1

                query = '.value[@key="foreignKeys"]/value[@struct-name="db.mysql.ForeignKey"]'
                for fk_element in table_element.findall(query):
                    fk = self.__get_foreign_key(fk_element)
                    fk.table_ref = table.id
                    table.foreign_keys.append(fk)

                query = '.value[@key="indices"]/value[@struct-name="db.mysql.Index"]'
                for index_element in table_element.findall(query):
                    index = self.__get_index(index_element)
                    index.table_ref = table.id
                    table.indexes.append(index)

        return schemas


    @staticmethod
    def __get_schema(schema_element):
        schema_id = schema_element.get('id').strip('{}').lower()
        name = schema_element.find('.value[@key="name"]').text.encode('utf8')
        comment = schema_element.find('.value[@key="comment"]').text
        collation = schema_element.find('.value[@key="defaultCollationName"]').text

        if comment:
            comment = comment.encode('utf8')

        return Schema(id=schema_id, database_name=name, comment=comment, collation=collation)


    @staticmethod
    def __get_table(table_element):
        table_id = table_element.get('id').strip('{}').lower()
        name = table_element.find('.value[@key="name"]').text.encode('utf8')
        comment = table_element.find('.value[@key="comment"]').text
        if comment:
            comment = comment.encode('utf8')

        return Table(id=table_id, name=name, comment=comment)

    @staticmethod
    def __get_index(index_element):
        index_id = index_element.get('id').strip('{}').lower()
        name = index_element.find('.value[@key="name"]').text
        index_type = index_element.find('.value[@key="indexType"]').text
        column_elements = index_element.findall('.value[@key="columns"]/value[@struct-name="db.mysql.IndexColumn"]')
        columns = [el.find('.link[@key="referencedColumn"]').text for el in column_elements]
        return Index(name=name, storage_type=index_type, columns=columns, id=index_id)

    def __get_column(self, column_element, ordinal=sys.maxint):
        column_id = column_element.get('id').strip('{}').lower()
        name = column_element.find('.value[@key="name"]').text
        nullable = int(column_element.find('.value[@key="isNotNull"]').text) is 0
        auto_increment = int(column_element.find('.value[@key="autoIncrement"]').text) is 0
        default_value = column_element.find('.value[@key="defaultValue"]').text
        comment = column_element.find('.value[@key="comment"]').text
        length = column_element.find('.value[@key="length"]').text
        precision = column_element.find('.value[@key="precision"]').text
        if comment:
            comment = comment.encode('utf8')
        workbench_type = None

        user_element = column_element.find('.link[@key="userType"]')

        if user_element is not None:
            user_type = self.user_types[user_element.text]
            sql_type = user_type['sql']
            workbench_type = user_type['name']
        else:
            sql_type = self.__parse_simple_type(column_element)

        # todo type set sql_type for now. later change it to internal type maybe

        return Column(name=name, is_nullable=nullable,
                      default=default_value, column_type=sql_type,
                      length=length, precision=precision, is_auto_increment=auto_increment,
                      comment=comment, ordinal=ordinal, id=column_id)

    def __get_foreign_key(self, fk_element):
        fk_id = fk_element.get('id').strip('{}').lower()
        name = fk_element.find('.value[@key="name"]').text
        comment = fk_element.find('.value[@key="comment"]').text
        delete_rule = self.__parse_fk_rule(fk_element.find('.value[@key="deleteRule"]').text)
        update_rule = self.__parse_fk_rule(fk_element.find('.value[@key="updateRule"]').text)
        column_elements = fk_element.findall('.value[@key="columns"]/value[@struct-name="db.Column"]')
        columns = [el.find('.link').text for el in column_elements]
        ref_column_elements = fk_element.findall('.value[@key="columns"]/value[@struct-name="db.Column"]')
        ref_columns = [el.find('.link').text for el in ref_column_elements]

        return ForeignKey(name=name, id=fk_id, comment=comment,
                          on_delete_referential_action=delete_rule, on_update_referential_action=update_rule,
                          source_columns=columns, referenced_columns=ref_columns)

    @staticmethod
    def __parse_simple_type(column_element):
        data_type = column_element.find('.link[@key="simpleType"]')
        precision = column_element.find('.value[@key="precision"]').text
        length = column_element.find('.value[@key="length"]').text
        scale = column_element.find('.value[@key="scale"]').text
        option_list = [item for item in [precision, length, scale] if int(item) != -1]

        sql_data_type = data_type.text.split('.')[-1].upper()
        if len(option_list) > 0:
            sql_data_type = sql_data_type + "({0})".format(",".join(option_list))
        return sql_data_type

    def __parse_model_user_types(self):
        elements = self.model.findall('.//value[@key="userDatatypes"]/value')
        user_types = {}
        for el in elements:
            user_type = {
                'id': el.get('id'),
                'sql': el.find('.value[@key="sqlDefinition"]').text,
                'name': el.find('.value[@key="name"]').text,
            }
            user_types[user_type['id']] = user_type

        return user_types

    def __parse_fk_rule(self, rule):
        select = [x for x in REFERENTIAL_ACTIONS if x[1] == rule][0]
        return select[0]

    @staticmethod
    def __unpack_model(path):
        zip_file = ZipFile(path)
        return zip_file.read("document.mwb.xml")

