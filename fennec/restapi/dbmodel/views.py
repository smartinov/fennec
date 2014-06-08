from rest_framework import viewsets
from rest_framework.decorators import action
from fennec.restapi.versioncontroll.models import Change, Sandbox
from fennec.restapi.versioncontroll.serializers import ChangeSerializerAlt
from models import Namespace, Table, Column
from serializers import NamespaceSerializer, TableSerializer, ColumnSerializer
from rest_framework.request import Request


class SandboxAddin():
    def pre_save(self, obj):
        user = self.request.user
        branch_id = self.request.DATA['branch_id']
        obj.sandbox_ref = Sandbox.obtain_sandbox(user, branch_id)

class NamespaceViewSet(viewsets.ModelViewSet):
    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer


class TableViewSet(SandboxAddin, viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer





