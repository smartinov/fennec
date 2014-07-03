from rest_framework import viewsets
from models import Namespace, Table, Column
from serializers import NamespaceSerializer, TableSerializer, ColumnSerializer
from fennec.restapi.dbmodel.addins import SandboxAddin, ChangeAddin


class NamespaceViewSet(ChangeAddin, SandboxAddin, viewsets.ModelViewSet):
    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer


class TableViewSet(ChangeAddin, SandboxAddin, viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ColumnViewSet(ChangeAddin, SandboxAddin, viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer





