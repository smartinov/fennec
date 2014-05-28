from rest_framework import viewsets

from models import Diagram, Layer, TableSymbol, ColumnSymbol
from serializers import DiagramSerializer, LayerSerializer, TableSymbolSerializer, ColumnSymbolSerializer


class DiagramViewSet(viewsets.ModelViewSet):
    queryset = Diagram.objects.all()
    serializer_class = DiagramSerializer


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer


class TableSymbolViewSet(viewsets.ModelViewSet):
    queryset = TableSymbol.objects.all()
    serializer_class = TableSymbolSerializer


class ColumnSymbolViewSet(viewsets.ModelViewSet):
    queryset = ColumnSymbol.objects.all()
    serializer_class = ColumnSymbolSerializer