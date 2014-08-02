from django.db import models
from django.conf import settings

CHANGE_TYPE = (
    (0, "ADD"),
    (1, "MODIFY"),
    (2, "REMOVE")
)
SANDBOX_STATUS = (
    (0, "OPEN"),
    (1, "CLOSED")
)
REFERENTIAL_ACTIONS = (
    (0, "NO ACTION"),
    (1, "RESTRICT "),
    (2, "CASCADE "),
    (3, "SET NULL "),
)

class Namespace(models.Model):
    id = models.AutoField(primary_key=True)
    abbreviation = models.CharField(max_length=4, blank=True, help_text="namespace name abbreviation")
    name = models.CharField(max_length=45, help_text="namespace full name")
    description = models.TextField(default="", help_text="namespace description")
    parent_ref = models.ForeignKey('Namespace', help_text="parent namespace reference")
    project_ref = models.ForeignKey('Project', help_text="project reference")
    # TODO Implement: namespace.abbreviation unique within project


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True, default=lambda: generate_table_name(), help_text="Table name")
    description = models.TextField(default="", help_text="table description")
    collation = models.CharField(max_length=20, default="utf8_general_ci", help_text="table collation")
    namespace_ref = models.ForeignKey('Namespace',  help_text="namespace reference", blank=True, null=True)

    # TODO Implement: table.name unique within same namespace


class Column(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True, default=lambda: generate_column_name(), help_text="Table name")
    data_type = models.CharField(max_length=25, default="VARCHAR", help_text="column data type")
    length = models.IntegerField(help_text="length of data type")
    default_value = models.CharField(max_length=45, help_text="column default value")
    ordinal = models.IntegerField(help_text="ordinal of column within table")
    description = models.TextField(default="", help_text="column description")
    collation = models.CharField(max_length=20, default="utf8_general_ci", help_text="table collation")
    is_primary_key = models.BooleanField(default=False)
    is_nullable = models.BooleanField(default=False)
    is_unique = models.BooleanField(default=False)
    is_auto_increment = models.BooleanField(default=False)
    table_ref = models.ForeignKey('Table', help_text="table reference")

    # TODO Implement: table.name unique within same namespace


class ForeignKey(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    on_update_referential_action = models.SmallIntegerField(choices=REFERENTIAL_ACTIONS, default=0, help_text="referential action")
    on_delete_referential_action = models.SmallIntegerField(choices=REFERENTIAL_ACTIONS, default=0, help_text="referential action")
    table_ref = models.ForeignKey('Table', help_text="table reference")


def generate_table_name():
    #should be filtered by namespace_ref
    return "Table_{0}".format(Table.objects.all().count())


def generate_column_name():
    #should be filtered by table_ref
    return "Column_{0}".format(Column.objects.all().count())


class Diagram(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, default="Diagram")
    description = models.TextField(default="", help_text="diagram description")
    project_ref = models.ForeignKey('Project', help_text="project reference")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class Layer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, default="Layer")
    color_code = models.CharField(max_length=7, default="#CCFFFF", help_text="hex code in #000000 format")
    diagram_ref = models.ForeignKey('Diagram', help_text="owning diagram reference")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class TableSymbol(models.Model):
    id = models.AutoField(primary_key=True)
    position_x = models.FloatField()
    position_y = models.FloatField()
    width = models.FloatField(default=100)
    height = models.FloatField(default=100)
    color = models.CharField(max_length=6)
    is_collapsed = models.BooleanField()
    layer_ref = models.ForeignKey('Layer', null=True, help_text="if table is located on layer,"
                                                                "this field references the layer")
    diagram_ref = models.ForeignKey('Diagram', null=False, help_text="references diagram that contains table symbol")
    table_ref = models.ForeignKey('Table', null=False, help_text="references table model that this symbol represents")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class ColumnSymbol(models.Model):
    id = models.AutoField(primary_key=True)
    ordinal = models.SmallIntegerField(default=0, help_text="ordinal number of column within table")
    is_visible = models.BooleanField(default=True, help_text="flags if column should be shown or not")
    table_symbol_ref = models.ForeignKey('TableSymbol', help_text="owning table symbol")
    column_ref = models.ForeignKey('Column', help_text="references a column to represent")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class RelationshipSymbol(models.Model):
    id = models.AutoField(primary_key=True)
    start_column_symbol_ref = models.ForeignKey('ColumnSymbol', help_text="references start point of a relationship")
    start_column_symbol_ref = models.ForeignKey('ColumnSymbol', help_text="references end point of a relationship")
    draw_style = models.SmallIntegerField(default=0, help_text="defines a style for drawing of relationship symbol")
    foreign_key_ref = models.ForeignKey('ForeignKey', help_text="references foreign key that is represented "
                                                                "by this relationship")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the project")
    description = models.CharField(max_length=512, help_text="description of the project")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="project author")
    is_deleted = models.BooleanField(default=False)


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text="name of the branch")
    type = models.CharField(max_length=25, help_text="type of branch: feature/hotfix/etc")
    description = models.CharField(max_length=512, help_text="description of the branch")
    current_version = models.IntegerField(default=0)
    project_ref = models.ForeignKey('Project', help_text="project reference")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="branch author")
    parent_branch_revision = models.ForeignKey('BranchRevision', help_text="represents a branch revision that is "
                                                                           "a starting point of this branch.")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class BranchRevision(models.Model):
    id = models.AutoField(primary_key=True)
    revision_number = models.IntegerField(default=0, help_text="ordinal number of revision")
    previous_revision_ref = models.ForeignKey("BranchRevision", null=True,
                                              help_text="references previous revision of the same branch")
    branch_ref = models.ForeignKey(Branch, null=True, help_text="references owning branch")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class Change(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, help_text="change content containing the object of the change")
    object_type = models.CharField(max_length=25, help_text="type of object being changed")
    object_code = models.IntegerField(default=-1, help_text="references concrete object being changed")
    change_type = models.IntegerField(choices=CHANGE_TYPE, help_text="defines type of a change")
    is_ui_change = models.BooleanField(default=False, help_text="specifies if change is UI change of db model change")
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="change author")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


class SandboxChange(models.Model):
    id = models.AutoField(primary_key=True)
    sandbox_ref = models.ForeignKey('Sandbox', help_text="sandbox reference")
    change_ref = models.ForeignKey('Change', help_text="change reference")
    ordinal = models.IntegerField(default=0, help_text="ordinal number of change in change set")


class BranchRevisionChange(models.Model):
    id = models.AutoField(primary_key=True)
    branch_revision_ref = models.ForeignKey('BranchRevision', help_text="sandbox reference")
    change_ref = models.ForeignKey('Change', help_text="change reference")
    ordinal = models.IntegerField(default=0, help_text="ordinal number of change in change set")


class Sandbox(models.Model):
    id = models.AutoField(primary_key=True)
    bound_to_branch_ref = models.ForeignKey('Branch', help_text="references a branch for which the sandbox is used for")
    created_from_branch_revision_ref = models.ForeignKey('BranchRevision', help_text="references branch revision that "
                                                                        "is 'parent' to the sandbox")
    status = models.SmallIntegerField(choices=SANDBOX_STATUS, default=0,
                                      help_text="state of sandbox, opened or closed")
    is_deleted = models.SmallIntegerField(default=0, help_text="logical deletion")


    @staticmethod
    def obtain_sandbox(user, branch_id):
        branch = Branch.objects.get(pk=int(branch_id))
        sandbox = Sandbox.objects.filter(branch_ref=branch, accounts__id=user.id).first()
        if sandbox is None:
            sandbox = Sandbox()
            sandbox.branch_ref = branch
            sandbox.save()
            sandbox.accounts.add(user)
            sandbox.save()
        return sandbox

    def collect_changes(self):
        changes = []


        table_changes = Table.objects.filter(sandbox_ref=self)
        changes.extend(table_changes.all())
        changes.extend(Column.objects.filter(sandbox_ref=self).all())
        changes.extend(Namespace.objects.filter(sandbox_ref=self).all())
        return changes


    #def commit_changes(self):

