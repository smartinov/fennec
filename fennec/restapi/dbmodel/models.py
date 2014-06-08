from django.db import models
from fennec.restapi.versioncontroll.models import Project, Sandbox
# Create your models here.


class Namespace(models.Model):
    id = models.AutoField(primary_key=True)
    abbreviation = models.CharField(max_length=4, blank=True, help_text="namespace name abbreviation")
    name = models.CharField(max_length=45, help_text="namespace full name")
    description = models.TextField(default="", help_text="namespace description")
    parent_ref = models.ForeignKey('Namespace', help_text="parent namespace reference")
    project_ref = models.ForeignKey(Project, help_text="project reference")
    sandbox_ref = models.ForeignKey(Sandbox, help_text="sandbox_ref")
    # TODO Implement: namespace.abbreviation unique within project


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True, default=lambda: generate_table_name(), help_text="Table name")
    description = models.TextField(default="", help_text="table description")
    collation = models.CharField(max_length=20, default="utf8_general_ci", help_text="table collation")
    namespace_ref = models.ForeignKey(Namespace,  help_text="namespace reference", blank=True, null=True)
    sandbox_ref = models.ForeignKey(Sandbox, help_text="sandbox_ref")

    # TODO Implement: table.name unique within same namespace


class Column(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True, default=lambda: generate_column_name(), help_text="Table name")
    data_type = models.CharField(max_length=25, default="VARCHAR", help_text="column data type")
    length = models.IntegerField(help_text="length of data type")
    default_value = models.CharField(max_length=45, help_text="column default value")
    ordinal = models.IntegerField(help_text="ordinal of column within table")
    description = models.TextField(default="", help_text="column description")
    is_primary_key = models.BooleanField(default=False)
    is_nullable = models.BooleanField(default=False)
    is_unique = models.BooleanField(default=False)
    is_auto_increment = models.BooleanField(default=False)
    table_ref = models.ForeignKey('Table', help_text="table reference")
    sandbox_ref = models.ForeignKey(Sandbox, help_text="sandbox_ref")

    # TODO Implement: table.name unique within same namespace


def generate_table_name():
    #should be filtered by namespace_ref
    return "Table_{0}".format(Table.objects.all().count())


def generate_column_name():
    #should be filtered by table_ref
    return "Column_{0}".format(Column.objects.all().count())