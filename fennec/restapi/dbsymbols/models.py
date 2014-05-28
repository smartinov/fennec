from django.db import models
from fennec.restapi.dbmodel.models import Project, Column
from fennec.restapi import dbmodel
# Create your models here.


class Diagram(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, default="Diagram")
    description = models.TextField(default="", help_text="diagram description")
    project_ref = models.ForeignKey(Project, help_text="project reference")

    # TODO: diagram.name is unique per project


class Layer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, default="Layer")
    color_code = models.CharField(max_length=7, default="#CCFFFF", help_text="hex code in #000000 format")
    diagram_ref = models.ForeignKey(Diagram, help_text="owning diagram reference")


class TableSymbol(models.Model):
    id = models.AutoField(primary_key=True)
    position_x = models.FloatField()
    position_y = models.FloatField()
    width = models.FloatField(default=100)
    height = models.FloatField(default=100)
    color = models.CharField(max_length=6)
    is_collapsed = models.BooleanField()


class ColumnSymbol(models.Model):
    id = models.AutoField(primary_key=True)
    is_visible = models.BooleanField(default=True, help_text="flags if column should be shown or not")
    table_symbol_ref = models.ForeignKey(TableSymbol, help_text="owning table symbol")
    column_ref = models.ForeignKey(Column, help_text="references a column to represent")
